DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50

VERBOSE = 15
NORMAL = 20
QUIET = 25

class Logger:
    def __init__(self, level, **kwargs):
        if level is True:
            level = VERBOSE
        self.level = level
        self.defaults = kwargs
    def log(self, level, *args, **kwargs):
        if self.level is False or level < self.level:
            return
        print(*args, **kwargs, **self.defaults)
    def debug(self, *args, **kwargs):
        self.log(DEBUG, *args, **kwargs)
    def info(self, *args, **kwargs):
        self.log(INFO, *args, **kwargs)
    def warning(self, *args, **kwargs):
        self.log(WARNING, *args, **kwargs)
    def error(self, *args, **kwargs):
        self.log(ERROR, *args, **kwargs)
    def critical(self, *args, **kwargs):
        self.log(CRITICAL, *args, **kwargs)
    def verbose(self, *args, **kwargs):
        self.log(VERBOSE, *args, **kwargs)
    def normal(self, *args, **kwargs):
        self.log(NORMAL, *args, **kwargs)
    def quiet(self, *args, **kwargs):
        self.log(QUIET, *args, **kwargs)
