from typing import ClassVar


class ValidationExc(Exception):
    status_code: ClassVar[int] = 400
    code: ClassVar[str] = "validation_error"
    default_msg: ClassVar[str] = "Erro de validação."
    detail: dict[str, list[str]] | None = None


class NotAuthenticatedExc(Exception):
    status_code: ClassVar[int] = 401
    code: ClassVar[str] = "not_authenticated"
    default_msg: ClassVar[str] = "Usuário não autenticado."
    detail: dict[str, list[str]] | None = None


class PermissionDeniedExc(Exception):
    status_code: ClassVar[int] = 403
    code: ClassVar[str] = "permission_denied"
    default_msg: ClassVar[str] = "Permissão negada para o recurso solicitado."
    detail: dict[str, list[str]] | None = None


class NotFoundExc(Exception):
    status_code: ClassVar[int] = 404
    code: ClassVar[str] = "not_found"
    default_msg: ClassVar[str] = "Recurso procurado não encontrado."
    detail: dict[str, list[str]] | None = None


class ConflictExc(Exception):
    status_code: ClassVar[int] = 409
    code: ClassVar[str] = "conflict"
    default_msg: ClassVar[str] = "Um conflito ocorreu durante a solicitação."
    detail: dict[str, list[str]] | None = None


class ExpectationFailedExc(Exception):
    status_code: ClassVar[int] = 417
    code: ClassVar[str] = "expectation_failed"
    default_msg: ClassVar[str] = "Expectativa não atendida."
    detail: dict[str, list[str]] | None = None


class ServerErrorExc(Exception):
    status_code: ClassVar[int] = 500
    code: ClassVar[str] = "server_error"
    default_msg: ClassVar[str] = "Erro interno do servidor."
    detail: dict[str, list[str]] | None = None


class NotImplementedExc(Exception):
    status_code: ClassVar[int] = 501
    code: ClassVar[str] = "not_implemented"
    default_msg: ClassVar[str] = "Recurso solicitado ainda não foi implementado."
    detail: dict[str, list[str]] | None = None
