import logging
from typing import Self

from django.db import models

from shared.models.validators import make_aware_if_exists


class BaseModel(models.Model):
    """
    Abstract base model, for assurance more quality for system.
        Attributes:\n
        - id
        - created_at
        - updated_at
    """

    id = models.BigAutoField(primary_key=True, editable=False, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def clean(self) -> None:
        """
        Method to validate the model.
        """
        self.created_at = make_aware_if_exists(self.created_at)
        self.updated_at = make_aware_if_exists(self.updated_at)
        return None

    def save(self, *args: list, **kwargs: dict) -> Self:
        """
        Method to save the model.
        """
        self.clean()
        return super(BaseModel, self).save(*args, **kwargs)

    @classmethod
    def filter_by_search(
        cls,
        queryset: models.QuerySet,
        search_params: list[tuple[str, str]],
        search_fields: list[str],
    ) -> models.QuerySet:
        """
        Aplica filtros de pesquisa em um queryset do Django.
        Método de classe que permite filtrar um queryset baseado em parâmetros de busca específicos,
        suportando operadores de consulta do Django (como __gte, __contains, etc).
        Args:
            queryset (models.QuerySet): O queryset base a ser filtrado.
            search_params (list[tuple[str,str]]): Lista de tuplas contendo pares de (campo, valor) para filtrar.
            search_fields (list[str]): Lista de campos permitidos para busca.
        Returns:
            models.QuerySet: Queryset filtrado com os parâmetros de busca aplicados.
        Example:
            >>> search_params = [('nome__contains', 'João'), ('idade__gte', '18')]
            >>> search_fields = ['nome', 'idade']
            >>> Model.filter_by_search(Model.objects.all(), search_params, search_fields)
        """

        filters = models.Q()

        for field, value in search_params:
            try:
                if field in search_fields:
                    filters |= models.Q(**{f"{field}__icontains": value})
                if field.startswith(f"{field}__"):
                    filters |= models.Q(**{field: value})
            except Exception as e:
                logging.error(f"❌ Erro ao aplicar filtro '{field}::{value}': {e}")

        return queryset.filter(filters)

    class Meta:
        abstract = True
