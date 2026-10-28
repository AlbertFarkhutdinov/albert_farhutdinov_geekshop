"""The module provides logging utils."""

import json
import logging
import sys
from datetime import UTC, datetime


class JsonFormatter(logging.Formatter):
    """Logging formatter that outputs log records as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the LogRecord as a JSON string.

        Parameters
        ----------
        record : logging.LogRecord
            The log record to format.

        Returns
        -------
        str
            JSON-encoded string with ``Timestamp``, ``LogLevel``, and
            ``Message`` fields.

        """
        message = super().format(record)
        return json.dumps(
            {
                'Timestamp': datetime.fromtimestamp(
                    timestamp=record.created,
                    tz=UTC,
                ).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'LogLevel': record.levelname,
                'Message': message,
            },
            ensure_ascii=False,
        )


def set_logging_config(level: int = logging.INFO) -> None:
    """
    Set the logging configuration.

    Configures the root logger with a :class:`JsonFormatter` and a
    ``stdout`` stream handler.

    Parameters
    ----------
    level : int, default: logging.INFO
        Logging level to apply to the root logger.

    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(JsonFormatter())
    root_logger.addHandler(stream_handler)


LOGGER_NAME = 'default'
logging_uvicorn_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        LOGGER_NAME: {
            '()': JsonFormatter,
        },
    },
    'handlers': {
        LOGGER_NAME: {
            'formatter': LOGGER_NAME,
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    },
    'loggers': {
        'uvicorn': {
            'handlers': [LOGGER_NAME],
            'level': 'INFO',
            'propagate': False,
        },
        'uvicorn.error': {'level': 'INFO'},
        'uvicorn.access': {
            'handlers': [LOGGER_NAME],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
