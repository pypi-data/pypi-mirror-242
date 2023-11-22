# coding=utf8
import linecache
import fcntl
import eventlet.debug
import os
import logging
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
import sys
import traceback

from aalam_common.config import cfg
from aalam_common import utils


MAX_CRASHES = 10

# the following code is taken from openstack/swift.
# the problem being - when the application creates a new thread
# and if from that thread there is a logging message, then it tries
# to acquire a green mutex which the actual logging implementation uses
# threading.Rlock, which is not thread sensitive and gets hung
class PipeMutex(object):
    def __init__(self):
        self.rfd, self.wfd = os.pipe2(os.O_NONBLOCK)
        os.write(self.wfd, b'-')  # start unlocked
        self.owner = None
        self.recursion_depth = 0
        eventlet.debug.hub_prevent_multiple_readers(False)

    def acquire(self, blocking=True):
        current_greenthread_id = id(eventlet.greenthread.getcurrent())
        if self.owner == current_greenthread_id:
            self.recursion_depth += 1
            return True

        while True:
            try:
                os.read(self.rfd, 1)
                self.owner = current_greenthread_id
                return True
            except OSError as err:
                if err.errno != errno.EAGAIN:
                    raise

                if not blocking:
                    return False

                trampoline(self.rfd, read=True)

    def release(self):
        current_greenthread_id = id(eventlet.greenthread.getcurrent())
        if self.owner != current_greenthread_id:
            raise RuntimeError("cannot release un-acquired lock")

        if self.recursion_depth > 0:
            self.recursion_depth -= 1
            return

        self.owner = None
        os.write(self.wfd, b'X')

    def close(self):
        if self.wfd is not None:
            os.close(self.rfd)
            self.rfd = None
            os.close(self.wfd)
            self.wfd = None
        self.owner = None
        self.recursion_depth = 0

    def __del__(self):
        self.close()


class ThreadSafeRotatingFileHandler(RotatingFileHandler):
    def createLock(self):
        self.lock = PipeMutex()


class StackReporter(object):
    def __init__(self, exc_frame, lineno):
        self.frame = exc_frame
        self.filename = exc_frame.f_code.co_filename
        self.lineno = lineno
        self.function = exc_frame.f_code.co_name

    def get_file_line(self, from_line):
        code = linecache.getline(self.filename, from_line,
                                 self.frame.f_globals)
        if code:
            code = code.rstrip('\n')

        return "%d: %s" % (from_line, code)

    def get_pre_context(self, num_lines):
        from_line = self.lineno - num_lines if self.lineno > num_lines else 0
        ret = []
        while from_line < self.lineno:
            ret.append(self.get_file_line(from_line))
            from_line += 1

        return ret

    def get_post_context(self, num_lines):
        from_line = self.lineno
        to_line = self.lineno + num_lines
        ret = []
        while from_line <= to_line:
            ret.append(self.get_file_line(from_line))
            from_line += 1

        return ret

    def get_locals(self):
        ret = []
        for (k, v) in self.frame.f_locals.items():
            if not (k.startswith('__') and k.endswith('__')):
                ret.append('{} = {}'.format(k, v))

        return ret

    def get_globals(self):
        ret = []
        for (k, v) in self.frame.f_globals.items():
            ret.append('{} = {}'.format(k, v))

        return ret


class ExceptionTraceback(object):
    def __init__(self, exc_type, exc_value, exc_tb):
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.exc_tb = exc_tb

    def format_exception(self):
        ret = ["Traceback of the most recent exception"]
        frame_num = 0
        tb = self.exc_tb
        ret += traceback.format_exception_only(self.exc_type, self.exc_value)
        ret += [' ----------------------------------------- ']
        while tb is not None:
            if tb.tb_frame.f_locals.get('__traceback_hide__'):
                tb = tb.tb_next
                continue

            stack = StackReporter(tb.tb_frame, tb.tb_lineno)
            ret += ["File %s, line %s, function %s" %
                    (stack.filename, stack.lineno, stack.function)]
            ret += [""]
            ret.extend(stack.get_locals())
            ret += [""]
            ret.extend(stack.get_pre_context(3))
            ret.extend(stack.get_post_context(3))
            ret += [' ----------- End of frame %d ------------- '
                    % (frame_num)]

            frame_num += 1
            tb = tb.tb_next
            stack = None

        return ret


def _except_hook(exc_type, exc_value, exc_tb):
    if exc_type == KeyboardInterrupt:
        return

    etb = ExceptionTraceback(exc_type, exc_value, exc_tb)
    lines = etb.format_exception()

    for line in lines:
        logging.critical(line)

    utils.report_bug("crash", exc_type, exc_value, lines)
    # The supervising deamon will not restart if this app crashed more
    # than 10 time in 5 minutes
    crash_count = os.path.join("/tmp", "%s_%s.crash_count" % (
        cfg.CONF.app_provider_code, cfg.CONF.app_code))
    curr_count = 0
    if not os.path.exists(crash_count):
        open_mode = "w"
    else:
        mtime = datetime.fromtimestamp(os.path.getmtime(crash_count))
        if (mtime > datetime.now() - timedelta(minutes=5)):
            open_mode = "r+"
        else:
            open_mode = "w"
    with open(crash_count, open_mode) as fd: 
        curr_count = int(fd.read()) if open_mode == 'r+' else 0
        logging.critical("App crashed - current crash count = %s" % curr_count)
        curr_count += 1
        fd.seek(0)
        fd.write(str(curr_count))
    if curr_count >= MAX_CRASHES:
        # lets wait for 10 crashes to see if the app recovers, \
        # after which we stop it for good
        os.unlink(crash_count)
        logging.critical("App crashed more than 10 times, stopping it now")
        path = os.path.join("/tmp", "%s_%s.stop" % (
            cfg.CONF.app_provider_code, cfg.CONF.app_code))
        with open(path, "w"):
            pass


def init_logging(logger):
    cfg_debug = getattr(cfg.CONF, "debug", None)
    ll = getattr(
        logging, cfg.CONF.debug.log_level.upper() if cfg_debug else "DEBUG")
    if cfg_debug and getattr(cfg_debug, "log_file", None):
        lh = ThreadSafeRotatingFileHandler(cfg_debug.log_file,
                                 maxBytes=1048576,
                                 encoding='utf-8',
                                 backupCount=3)
        FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        lh.setFormatter(logging.Formatter(FORMAT))
        logger.addHandler(lh)

    logger.setLevel(ll)


class StreamLog(object):
    def __init__(self, logger, log_level):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        self.logger.log(self.log_level, "\n")


# init_debug() should be called at the module initialization
# and only once. This will register for the logging,
# exception hooks, etc
def init_debug():
    sys.excepthook = _except_hook
    init_logging(logging.getLogger())
    cfg_debug = getattr(cfg.CONF, "debug", None)
    if cfg_debug and getattr(cfg_debug, "log_file", None):
        sys.stdout = StreamLog(logging.getLogger('STDOUT'), logging.DEBUG)
        sys.stderr = StreamLog(logging.getLogger('STDERR'), logging.ERROR)
