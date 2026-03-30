import logging
import json
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),  # The .isoformat() makes it a string!,
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            # Use environment variables (Month 1 Week 4 prep)
            "service": os.getenv("SERVICE_NAME", "ai-llm-service"),
            "env": os.getenv("APP_ENV", "dev"),
        }

        # IMPROVEMENT: Automatically merge ANY extra fields without 'extra_data' key
        # This makes your decorators much cleaner.
        standard_attrs = (
            "args",
            "asctime",
            "created",
            "exc_info",
            "exc_text",
            "filename",
            "funcName",
            "levelname",
            "levelno",
            "lineno",
            "module",
            "msecs",
            "msg",
            "name",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "stack_info",
            "thread",
            "threadName",
        )

        for key, value in record.__dict__.items():
            if key not in standard_attrs:
                log_record[key] = value

        return json.dumps(log_record)


class AppLogger:
    _logger = None

    @classmethod
    def get_logger(cls, file_path: str = "logs/app.log"):
        if cls._logger is None:
            # 1. Resolve absolute path to avoid "disappearing" files
            log_path = Path(file_path).resolve()
            log_path.parent.mkdir(parents=True, exist_ok=True)

            logger = logging.getLogger("app_llm_engineer")  # Unique name
            logger.setLevel(logging.INFO)
            logger.propagate = False  # Prevent double logging to console

            # 2. Clear existing handlers to prevent duplicates during dev
            if logger.hasHandlers():
                logger.handlers.clear()

            # 3. Setup File Handler
            file_handler = TimedRotatingFileHandler(
                str(log_path),
                when="midnight",
                interval=1,
                backupCount=30,
                encoding="utf-8",
            )
            file_handler.setFormatter(JsonFormatter())
            logger.addHandler(file_handler)

            cls._logger = logger

        return cls._logger
