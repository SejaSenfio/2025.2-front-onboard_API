import ast
import logging
import traceback
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable

import sentry_sdk
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import IntegrityError
from django.http import Http404
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import APIException, AuthenticationFailed, ErrorDetail
from rest_framework.exceptions import ValidationError as DRFValidationError

from shared.exceptions.base import (
    ConflictExc,
    ExpectationFailedExc,
    NotAuthenticatedExc,
    NotFoundExc,
    NotImplementedExc,
    PermissionDeniedExc,
    ServerErrorExc,
    ValidationExc,
)
from shared.exceptions.nutcracker import PydanticValidationErrorNutcracker

from .serializers import ApiErrorSerializer


@dataclass(kw_only=True, slots=True, frozen=True)
class _Handler:
    exc: Any
    context: Any

    @staticmethod
    def match(accept_exceptions: list[type[Exception]]) -> Callable[..., Any]:
        def decorator(func: Callable) -> Any:
            @wraps(func)
            def wrapper(self: Any, *args: list, **kwargs: dict) -> Any:
                for exc_type in accept_exceptions:
                    if isinstance(self.exc, exc_type):
                        return func(self, *args, exc_received=self.exc, **kwargs)
                return None

            return wrapper

        return decorator

    def handle(self, *args: list, **kwargs: dict) -> tuple[dict, int]:
        raise NotImplementedError

    def _process_exception_response(
        self, data: dict, status_code: int
    ) -> tuple[dict[str, str], int]:
        try:
            logging.debug(f"APIResponse - Data: {data}, Status Code: {status_code}")

            data["message"] = data["message"]
            if data.get("errors"):
                data["errors"] = {
                    key: [value for value in values] for key, values in data["errors"].items()
                }

            serializer = ApiErrorSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            response = serializer.validated_data, status_code
            return response
        except DRFValidationError as error:
            logging.critical(f"Problemas ao retornar erro na api: {error}")
            with sentry_sdk.push_scope() as scope:
                scope.set_context("context", self.context)
                sentry_sdk.capture_exception(error)
            return {
                "code": ServerErrorExc.code,
                "message": ServerErrorExc.default_msg,
            }, ServerErrorExc.status_code

    def _generate_base_data(
        self, code: str, default_msg: str, exc_received: Exception
    ) -> dict[str, str | list[str] | dict[str, str]]:
        data: dict[str, str | list[str] | dict[str, str]] = {"code": code}

        message_posted = str(exc_received).strip()
        if not message_posted.strip():
            data["message"] = default_msg
        elif message_posted.startswith("{"):
            data["message"] = default_msg
            try:
                data["errors"] = ast.literal_eval(message_posted)
            except Exception as exc:
                logging.debug(f"Erro ao converter detalhes de erro({message_posted}): {exc}")
        else:
            data["message"] = message_posted

        return data


class ValidationErrorHandler(_Handler):
    @_Handler.match(
        accept_exceptions=[ValidationExc, IntegrityError, PydanticValidationError, ValueError]
    )
    def handle(self, exc_received: Exception, *args: list, **kwargs: dict) -> tuple[dict, int]:
        logging.debug(
            f"Handling ValidationExc: {exc_received} | Args: {args} | Kwargs: {kwargs} | Context: {self.context}"
        )
        if isinstance(exc_received, PydanticValidationError):
            exc_received = ValidationExc(PydanticValidationErrorNutcracker.get_errors(exc_received))

        data = self._generate_base_data(
            code=ValidationExc.code,
            default_msg=ValidationExc.default_msg,
            exc_received=exc_received,
        )

        return self._process_exception_response(data=data, status_code=ValidationExc.status_code)


class PermissionDeniedHandler(_Handler):
    @_Handler.match(accept_exceptions=[PermissionDeniedExc, PermissionDenied])
    def handle(self, exc_received: Exception, *args: list, **kwargs: dict) -> tuple[dict, int]:
        logging.debug(
            f"Handling ValidationExc: {exc_received} | Args: {args} | Kwargs: {kwargs} | Context: {self.context}"
        )
        data = self._generate_base_data(
            code=PermissionDeniedExc.code,
            default_msg=PermissionDeniedExc.default_msg,
            exc_received=exc_received,
        )
        return self._process_exception_response(
            data=data, status_code=PermissionDeniedExc.status_code
        )


class NotAuthenticatedHandler(_Handler):
    @_Handler.match(accept_exceptions=[NotAuthenticatedExc, AuthenticationFailed])
    def handle(self, exc_received: Exception, *args: list, **kwargs: dict) -> tuple[dict, int]:
        logging.debug(
            f"Handling ValidationExc: {exc_received} | Args: {args} | Kwargs: {kwargs} | Context: {self.context}"
        )
        data = self._generate_base_data(
            code=NotAuthenticatedExc.code,
            default_msg=NotAuthenticatedExc.default_msg,
            exc_received=exc_received,
        )
        return self._process_exception_response(
            data=data, status_code=NotAuthenticatedExc.status_code
        )


class ConflictHandler(_Handler):
    @_Handler.match(accept_exceptions=[ConflictExc])
    def handle(self, exc_received: Exception, *args: list, **kwargs: dict) -> tuple[dict, int]:
        logging.debug(
            f"Handling ValidationExc: {exc_received} | Args: {args} | Kwargs: {kwargs} | Context: {self.context}"
        )
        data = self._generate_base_data(
            code=ConflictExc.code, default_msg=ConflictExc.default_msg, exc_received=exc_received
        )
        return self._process_exception_response(data=data, status_code=ConflictExc.status_code)


class ExpectationFailedHandler(_Handler):
    @_Handler.match(accept_exceptions=[ExpectationFailedExc])
    def handle(self, exc_received: Exception, *args: list, **kwargs: dict) -> tuple[dict, int]:
        logging.debug(
            f"Handling ValidationExc: {exc_received} | Args: {args} | Kwargs: {kwargs} | Context: {self.context}"
        )
        data = self._generate_base_data(
            code=ExpectationFailedExc.code,
            default_msg=ExpectationFailedExc.default_msg,
            exc_received=exc_received,
        )
        return self._process_exception_response(
            data=data, status_code=ExpectationFailedExc.status_code
        )


class ApiExceptionHandler(_Handler):
    @_Handler.match(accept_exceptions=[APIException, DRFValidationError])
    def handle(self, exc_received: Exception, *args: list, **kwargs: dict) -> tuple[dict, int]:
        logging.debug(
            f"Handling ValidationExc: {exc_received} | Args: {args} | Kwargs: {kwargs} | Context: {self.context}"
        )
        data = {
            "code": getattr(exc_received, "code", getattr(exc_received, "default_code", "error")),
            "message": "Requisição inválida.",
        }

        if exc_detail := getattr(exc_received, "detail"):
            if isinstance(exc_detail, dict):
                data["errors"] = {
                    key: [str(value) for value in values] for key, values in exc_detail.items()
                }
            elif isinstance(exc_detail, ErrorDetail):
                data["message"] = str(exc_detail)
            else:
                logging.warning("Exceção sem detalhes estruturados.")

        return self._process_exception_response(
            data=data, status_code=getattr(exc_received, "status_code", 400)
        )


class NotFoundHandler(_Handler):
    @_Handler.match(accept_exceptions=[NotFoundExc, ObjectDoesNotExist, Http404])
    def handle(self, exc_received: Exception, *args: list, **kwargs: dict) -> tuple[dict, int]:
        logging.debug(
            f"Handling ValidationExc: {exc_received} | Args: {args} | Kwargs: {kwargs} | Context: {self.context}"
        )
        if isinstance(exc_received, (ObjectDoesNotExist, Http404)):
            exc_received = (
                NotFoundExc()
            )  # Esse shift acontece pq a msg do erro é pouco expressiva, portanto é melhor usar a padrão da NotFoundExc.
        data = self._generate_base_data(
            code=NotFoundExc.code, default_msg=NotFoundExc.default_msg, exc_received=exc_received
        )
        return self._process_exception_response(data=data, status_code=NotFoundExc.status_code)


class NotImplementedHandler(_Handler):
    @_Handler.match(accept_exceptions=[NotImplementedExc])
    def handle(self, exc_received: Exception, *args: list, **kwargs: dict) -> tuple[dict, int]:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("context", self.context)
            sentry_sdk.capture_exception(exc_received)

        logging.debug(
            f"Handling ValidationExc: {exc_received} | Args: {args} | Kwargs: {kwargs} | Context: {self.context}"
        )
        data = self._generate_base_data(
            code=NotImplementedExc.code,
            default_msg=NotImplementedExc.default_msg,
            exc_received=exc_received,
        )
        sentry_sdk.capture_exception(exc_received)
        return self._process_exception_response(
            data=data, status_code=NotImplementedExc.status_code
        )


class GeneralExceptionHandler(_Handler):
    @_Handler.match(accept_exceptions=[Exception])
    def handle(self, exc_received: Exception, *args: list, **kwargs: dict) -> tuple[dict, int]:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("context", self.context)
            sentry_sdk.capture_exception(exc_received)

        logging.critical(
            f"Unhandled exception:\n"
            f"Exception: {exc_received}\n"
            f"Type: {type(exc_received).__name__}\n"
            f"Traceback:\n{''.join(traceback.format_tb(exc_received.__traceback__))}"
        )
        data = {"code": ServerErrorExc.code, "message": ServerErrorExc.default_msg}
        return self._process_exception_response(data=data, status_code=ServerErrorExc.status_code)
