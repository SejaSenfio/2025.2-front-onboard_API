from .base import ConflictExc, NotFoundExc


class NoLinksFound(NotFoundExc): ...


class TagAlreadyLinked(ConflictExc): ...
