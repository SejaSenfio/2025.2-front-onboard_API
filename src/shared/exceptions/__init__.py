from .base import (
    ConflictExc,
    ExpectationFailedExc,
    NotAuthenticatedExc,
    NotFoundExc,
    NotImplementedExc,
    PermissionDeniedExc,
    ServerErrorExc,
    ValidationExc,
)
from .dependencies import DependencyNotFound
from .entities import EntityNotFound
from .integrity import CantDeleteEntityWithEvents
from .permissions import PermissionCustomNotFoundException
from .queries import InvalidQueryParamsError
from .sms import (
    SmsBaseException,
    SmsRequestException100,
    SmsRequestException101,
    SmsRequestException102,
    SmsRequestException103,
    SmsRequestException104,
    SmsRequestException105,
    SmsRequestException106,
    SmsRequestException107,
)
from .tag_links import NoLinksFound, TagAlreadyLinked

__all__ = [
    "ConflictExc",
    "ExpectationFailedExc",
    "NotAuthenticatedExc",
    "NotFoundExc",
    "NotImplementedExc",
    "PermissionDeniedExc",
    "ServerErrorExc",
    "ValidationExc",
    "DependencyNotFound",
    "EntityNotFound",
    "CantDeleteEntityWithEvents",
    "PermissionCustomNotFoundException",
    "InvalidQueryParamsError",
    "SmsBaseException",
    "SmsRequestException100",
    "SmsRequestException101",
    "SmsRequestException102",
    "SmsRequestException103",
    "SmsRequestException104",
    "SmsRequestException105",
    "SmsRequestException106",
    "SmsRequestException107",
    "NoLinksFound",
    "TagAlreadyLinked",
]
