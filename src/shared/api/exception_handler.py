from dataclasses import dataclass
from typing import Any, ClassVar

from rest_framework.response import Response

from .handlers import (
    ApiExceptionHandler,
    ConflictHandler,
    ExpectationFailedHandler,
    GeneralExceptionHandler,
    NotAuthenticatedHandler,
    NotFoundHandler,
    NotImplementedHandler,
    PermissionDeniedHandler,
    ValidationErrorHandler,
    _Handler,
)


def api_exceptions(exc: Any, context: Any) -> Response:
    router = _Router(exc, context)
    return router.handle_exception()


@dataclass
class _Router:
    exc: Any
    context: Any

    _handlers: ClassVar[list[type[_Handler]]] = [
        ValidationErrorHandler,
        NotAuthenticatedHandler,
        PermissionDeniedHandler,
        NotFoundHandler,
        ConflictHandler,
        ExpectationFailedHandler,
        ApiExceptionHandler,
        NotImplementedHandler,
    ]
    _end_chain_handler: ClassVar[type[_Handler]] = GeneralExceptionHandler

    def handle_exception(self) -> Response:
        for handler in self._handlers:
            if returned := handler(exc=self.exc, context=self.context).handle():
                data, status = returned
                return Response(data, status=status)

        ## GeneralExceptionHandler
        data, status = self._end_chain_handler(exc=self.exc, context=self.context).handle()
        return Response(data, status=status)
