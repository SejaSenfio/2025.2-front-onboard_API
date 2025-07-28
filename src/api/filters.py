import logging

from django.db import models
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.views import View


class FieldSearchFilter(SearchFilter):
    """
    Classe que estende SearchFilter para permitir pesquisas específicas por campo.
    Esta classe modifica o comportamento padrão do SearchFilter do DRF para suportar
    pesquisas no formato "campo::valor", permitindo buscas mais precisas em campos específicos.
    Attributes:
        Não possui atributos próprios, herda de SearchFilter
    Methods:
        filter_queryset: Filtra o queryset baseado nos parâmetros de busca fornecidos
    Exemplo de uso:
        Para pesquisar por nome::João e email::exemplo@email.com:
        ?search=nome::João;email::exemplo@email.com
    Requisitos:
        - O modelo deve implementar o método 'filter_by_search'
        - Os campos de pesquisa devem estar definidos em search_fields da view
        - O formato da busca deve ser 'campo::valor', separados por ';' para múltiplos campos
    Notas:
        - Campos inválidos ou mal formatados são ignorados com avisos no log
        - Se não houver '::' na string de busca, reverte para o comportamento padrão do SearchFilter
    """

    def filter_queryset(
        self, request: Request, queryset: models.QuerySet, view: View
    ) -> models.QuerySet:
        search_str = request.query_params.get("search", "").strip()

        if not search_str or "::" not in search_str:
            return super(FieldSearchFilter, self).filter_queryset(request, queryset, view)

        search_fields = getattr(view, "search_fields", [])
        search_params = search_str.split(";")

        # 🔹 Busca o modelo da queryset automaticamente
        model_class = queryset.model if queryset is not None else None

        if not model_class or not hasattr(model_class, "filter_by_search"):
            logging.warning(
                f"⚠️ O modelo '{model_class}' não tem o método 'filter_by_search'. Ignorando pesquisa."
            )
            return queryset

        # 🔹 Processa os filtros garantindo que não haja erros
        valid_search_params = []
        for param in search_params:
            try:
                field, value = param.split("::", 1)  # Divide corretamente o parâmetro
                field, value = field.strip(), value.strip()

                ALLOWED_LOOKUPS = [
                    "exact",
                    "iexact",
                    "contains",
                    "icontains",
                    "startswith",
                    "istartswith",
                    "endswith",
                    "iendswith",
                    "gt",
                    "gte",
                    "lt",
                    "lte",
                ]

                def is_valid_field_pattern(field_name: str) -> bool:
                    if field_name in search_fields:
                        return True
                    if "__" in field_name:
                        _, lookup = field_name.split("__", 1)
                        return lookup in ALLOWED_LOOKUPS
                    return False

                if is_valid_field_pattern(field):
                    valid_search_params.append((field, value))
                else:
                    logging.warning(
                        f"⚠️ Campo '{field}' não permitido para pesquisa na view {view.__class__.__name__}."
                    )

            except ValueError:
                logging.error(f"❌ Parâmetro de busca mal formatado: {param}. Ignorando.")
                continue

        # 🔹 Aplica a filtragem chamando `filter_by_search` do modelo automaticamente
        return model_class.filter_by_search(
            queryset=queryset, search_params=valid_search_params, search_fields=search_fields
        )
