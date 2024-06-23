import logging
import sys
from logging import LogRecord

COLORS = {
    "CRITICAL": "\033[95m",
    "ERROR": "\033[91m",
    "WARNING": "\033[93m",
    "INFO": "\033[92m",
    "DEBUG": "\033[94m",
    "RESET": "\033[0m",
}


class ColorFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        levelname = record.levelname
        if levelname in COLORS:
            levelname_color = COLORS[levelname] + levelname + COLORS["RESET"]
            record.levelname = levelname_color
        return super().format(record)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = ColorFormatter("%(levelname)s:     %(asctime)s - %(name)s - %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)
