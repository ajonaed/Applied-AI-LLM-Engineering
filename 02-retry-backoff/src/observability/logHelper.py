import logging
from logging import LoggerAdapter
from logging.handlers import TimedRotatingFileHandler


class AppLogger:
    __instance: LoggerAdapter = None

    @staticmethod
    def getInstance(filePath):
        if AppLogger.__instance == None:
            AppLogger.initLogger(filePath)
        return AppLogger.__instance

    @staticmethod
    def initLogger(filePath):
        # get a named global logger
        appLogger = logging.getLogger("root")
        appLogger.setLevel(logging.INFO)

        # configure console logging
        # interval=1 means the log rotation interval is 1
        # when='d' means the rotating interval will be in terms of days
        fileHandler = TimedRotatingFileHandler(
            filePath, backupCount=100, when="d", interval=1
        )
        # use namer function of the handler to keep the .log extension at the end of the file name
        fileHandler.namer = lambda name: name.replace(".log", "") + ".log"
        fmt = "%(asctime)s | %(levelname)s |  %(name)s | %(message)s"

        fileHandler.setFormatter(
            logging.Formatter(
                fmt,
                datefmt="%Y-%m-%d %H:%M:%S",  # 👈 no milliseconds
            )
        )
        appLogger.addHandler(fileHandler)

        AppLogger.__instance = LoggerAdapter(
            appLogger,
        )
