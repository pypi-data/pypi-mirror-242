import logging
import os
import errno


class MakeFileHandler(logging.FileHandler):
    """хэндлер, который создает папки для логов, если таких не существует"""

    def __init__(self, filename, mode="a", encoding=None, delay=0):
        self.mkdir_p(os.path.dirname(filename))
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)

    @staticmethod
    def mkdir_p(path):
        try:
            os.makedirs(path, exist_ok=True)
        except TypeError:
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise


LOGS_DIRECTORY = "logs"

CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "%(name)-12s %(levelname)-8s %(message)s"},
        "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
        "file": {
            "level": "INFO",
            "class": "config.settings.logging.MakeFileHandler",
            "formatter": "file",
            "filename": f"{LOGS_DIRECTORY}/debug.log",
        },
        "integration": {
            "level": "INFO",
            "class": "config.settings.logging.MakeFileHandler",
            "formatter": "file",
            "filename": f"{LOGS_DIRECTORY}/integration/sending.log",
        },
        "appeals_request": {
            "level": "INFO",
            "class": "config.settings.logging.MakeFileHandler",
            "formatter": "file",
            "filename": f"{LOGS_DIRECTORY}/appeals/requests.log",
        },
        "appeals_update": {
            "level": "INFO",
            "class": "config.settings.logging.MakeFileHandler",
            "formatter": "file",
            "filename": f"{LOGS_DIRECTORY}/appeals/updates.log",
        },
    },
    "loggers": {
        "": {"level": "DEBUG", "handlers": ["console"]},
        "appeals.request": {"level": "INFO", "handlers": ["appeals_request"]},
        "appeals.update": {"level": "INFO", "handlers": ["appeals_update"]},
        "integration.signals": {"level": "INFO", "handlers": ["integration"]},
    },
}
