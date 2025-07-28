import logging

import sentry_sdk
from pydantic import Field
from pydantic_settings import BaseSettings
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .base import DJANGO_SETT


class LogsSettings(BaseSettings):
    LOG_LEVEL: str = Field(default="INFO")
    SENTRY_DSN: str = Field(default="http://dummy:dummy@localhost/1")


LOGS_SETT = LogsSettings()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "{asctime} |[{levelname}] {filename}::{lineno}| {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "sentry": {
            "level": "WARNING",
            "class": "sentry_sdk.integrations.logging.EventHandler",
        },
    },
    "root": {
        "handlers": ["console", "sentry"],
        "level": "DEBUG" if DJANGO_SETT.DEBUG else LOGS_SETT.LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": ["console", "sentry"],
            "propagate": True,
        },
    },
}

sentry_sdk.init(
    dsn=LOGS_SETT.SENTRY_DSN,
    integrations=[
        DjangoIntegration(),
        LoggingIntegration(level=logging.INFO, event_level=logging.WARNING),
    ],
    send_default_pii=True,
)

# Configuração de logs para não poluir o console
logging.getLogger("_opentelemetry_tracing").setLevel(logging.ERROR)
logging.getLogger("factory").setLevel(logging.WARNING)
logging.getLogger("faker").setLevel(logging.WARNING)
logging.getLogger("factory.generate").setLevel(logging.WARNING)
