from .base import NotFoundExc


class PermissionCustomNotFoundException(NotFoundExc):
    """
    Exceção lançada quando uma permissão customizada não é encontrada para o codename fornecido.
    """

    pass
