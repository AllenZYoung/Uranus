# 关于日志记录的工具集
# by kahsolt

import os
from datetime import datetime
from app.utils.rootsUtils import BASE_DIR

class _LOG_LEVEL():
    def __init__(self):
        self.INFO = 'INFO'
        self.WARN = 'WARN'
        self.ERROR = 'ERROR'
        self.FATAL = 'FATAL'

LOG_FILE = os.path.join(BASE_DIR, 'Uranus/Uranus.log')
LOG_LEVEL = _LOG_LEVEL()


def log(msg='msg', src='src', level=LOG_LEVEL.INFO):
    out = logSilent(msg, src, level)
    print(out)


def logSilent(msg='msg', src='src', level=LOG_LEVEL.INFO):
    time = datetime.now()
    out = '[%s] %s\t<%s>: %s' %(level, time, src, msg)
    with open(LOG_FILE, 'a+') as logger:
        logger.write(out)
        logger.write('\r\n')
    return out