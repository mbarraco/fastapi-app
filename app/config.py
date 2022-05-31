import logging.config
import os
from typing import Any, Dict, Union

APP_DEBUG = bool(os.environ["APP_DEBUG"].lower() != "false")
DB_URL = os.environ["DB_URL"]
LOG_LEVEL = "DEBUG" if APP_DEBUG else "INFO"


LOGGING: Dict[str, Union[Dict[str, Any], bool, int, str]] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s: (%(name)s) %(message)s",
        }
    },
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        },
    },
    "root": {
        "handlers": ["default"],
        "level": LOG_LEVEL,
    },
}
logging.config.dictConfig(LOGGING)
