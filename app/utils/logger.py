import logging

COLORS = {
    "CRITICAL": "\033[95m",
    "ERROR": "\033[91m",
    "WARNING": "\033[93m",
    "INFO": "\033[92m",
    "DEBUG": "\033[94m",
    "RESET": "\033[0m",
}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            levelname_color = COLORS[levelname] + levelname + COLORS["RESET"]
            record.levelname = levelname_color
        return super().format(record)


logger = logging.getLogger()
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = ColorFormatter("%(levelname)s:    %(asctime)s - %(name)s - %(message)s")
ch.setFormatter(formatter)

logger.addHandler(ch)
