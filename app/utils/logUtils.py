# 关于日志记录的工具集
# by kahsolt

import os
import datetime
from Uranus.settings import BASE_DIR


class _LOG_LEVEL():
    def __init__(self):
        self.INFO = 'INFO'
        self.WARN = 'WARN'
        self.ERROR = 'ERROR'
        self.FATAL = 'FATAL'

LOG_FILE = os.path.join(BASE_DIR, 'Uranus/Uranus.log')
LOG_LEVEL = _LOG_LEVEL()


def log(src='functionName_or_shortDescription', msg='message_string', level=LOG_LEVEL.INFO):
    time = datetime.datetime.now()
    out = '[%s] %s\r\n<%s>: %s' %(level, time, src, msg)
    with open(LOG_FILE, 'a+') as logger:
        logger.write(out)
        logger.write('\r\n')
    print(out)
