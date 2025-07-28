from .base import ValidationExc


class InvalidQueryParamsError(ValidationExc):
    """Lançada quando os parâmetros de busca informados são inválidos."""

    ...
