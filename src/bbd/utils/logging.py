# coding : utf-8
# author : WONBEEN

from logging import (
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
    NOTSET,
    currentframe,
    getLogger,
    raiseExceptions,
    FileHandler,
    Formatter,
    Handler,
    StreamHandler
)


STDOUT = 15
STDERR = 45

class COLORS:
    RESET = '\033[0m'
    BLACK = '\033[30m'
    LGRAY="\033[0;37m"
    DGRAY="\033[1;30m"
    YELLOW = '\033[33m'
    B_CYAN = '\033[46m'
    B_YELLOW = '\033[43m'
    RED = '\033[31m'
    B_RED = '\033[31m'


class ConsoleFormatter(Formatter):
    """
    log 유형별 출력 스타일 지정
    """

    _LEVEL = '[%(levelname)s]'
    _FORMAT = ' [%(asctime)s][TwinDoc][%(name)s][%(lineno)s] %(message)s'

    FORMATS = {
        DEBUG: _LEVEL+_FORMAT,
        INFO: _LEVEL+_FORMAT,
        STDOUT: _LEVEL+_FORMAT,
        WARNING: COLORS.YELLOW+_LEVEL+COLORS.RESET+_FORMAT,
        ERROR: COLORS.RED+_LEVEL+COLORS.RESET+_FORMAT,
        STDERR: COLORS.RED+_LEVEL+COLORS.RESET+_FORMAT,
        CRITICAL: COLORS.B_RED+_LEVEL+COLORS.RESET+_FORMAT
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = Formatter(log_fmt)
        return formatter.format(record)

def get_logger(name):
    """
    logger 객체 반환.
    logger 객체에 ConsoleFormatter의 출력 설정을 불러오고, 저장할 log 파일을 지정한다.
    """
    logger = getLogger(name)
    logger.setLevel(DEBUG)

    console = StreamHandler()
    # console = TqdmLoggingHandler()
    console_formatter = ConsoleFormatter()
    console.setFormatter(console_formatter)
    # console.setStream(tqdm)
    logger.addHandler(console)

    log_file = 'bbd.log'
    file_handler = FileHandler(os.path.join('./', log_file), 'a')
    file_formatter = Formatter('[%(levelname)s] [bbd][%(asctime)s][%(name)s][%(lineno)s] %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger
