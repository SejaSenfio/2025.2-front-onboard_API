from typing import Any

from django.http.request import QueryDict
from rest_framework import serializers


class ApiErrorSerializer(serializers.Serializer):
    """
    Serializer para erros de API.
    """

    code = serializers.CharField(help_text="Código do erro")
    message = serializers.CharField(help_text="Mensagem de erro")
    errors = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField()),
        required=False,
        help_text="Detalhes do erro",
    )


class GenericResponseSerializer(serializers.Serializer):
    """
    Serializer genérico para respostas de API.
    """

    detail = serializers.CharField(help_text="Mensagem de detalhe da resposta")
    status = serializers.CharField(help_text="Status da resposta", required=False, allow_blank=True)
    data = serializers.DictField(
        child=serializers.CharField(),
        required=False,
        allow_null=True,
        help_text="Dados adicionais da resposta",
    )


class SearchListApiViewSerializer(serializers.Serializer):
    """
    Serializer para views de listagem com busca.
    Documenta o campo de busca e os campos de busca disponíveis.
    """

    search = serializers.CharField(required=False, help_text="Termo de busca")
    search_fields = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True,
        help_text="Campos de busca (uso interno, não documentado)",
    )

    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        search_fields = self.initial_data.get("search_fields", [])
        if search_fields:
            self.fields["search"].help_text = (
                f"Termo de busca para os campos: [ {', '.join(search_fields)} ]"
            )
        self.fields.pop("search_fields", None)


class OrderingListApiViewSerializer(serializers.Serializer):
    ordering = serializers.CharField(
        required=False,
        help_text="Campo(s) para ordenação",
    )
    ordering_fields = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True,
        help_text="Campos disponíveis para ordenação (uso interno, não documentado)",
    )

    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        ordering_fields = self.initial_data.get("ordering_fields", [])
        if ordering_fields:
            self.fields["ordering"].help_text = (
                f"Ordenação disponível para os campos: [ {', '.join(ordering_fields)} ]  (prefixo '-' para ordem decrescente)"
            )
        self.fields.pop("ordering_fields", None)


class StrictSerializer(serializers.Serializer):
    """
    Serializer para impedir parâmetros desconhecidos na requisição.\n
    Para o caso de parâmetros não conhecidos, o serializer retorna um erro listando-os.
    """

    def validate(self, attrs: dict) -> dict:
        declared_fields = set(self.fields.keys())
        received_fields = set(self.initial_data.keys())
        extra_fields = received_fields - declared_fields

        if extra_fields:
            formatted_fields = ",".join(f"'{field}'" for field in extra_fields)
            raise ValueError(f"Parâmetros desconhecidos: [{formatted_fields}]")

        return attrs


class NormalizedQueryParamsSerializer(serializers.Serializer):
    """
    Serializer para normalizar parâmetros de busca GET.\n
    No método GET, a busca de parâmetros retorna uma lista,
    portanto, precisa ser normalizada para ser passada como parâmetro,
    caso haja apenas um elemento na lista.
    """

    def to_internal_value(self, data: dict | QueryDict) -> Any:
        if isinstance(data, QueryDict):
            data = dict(data)

        normalized_data = {}
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                normalized_data[key] = value[0]
            else:
                normalized_data[key] = value

        return super(NormalizedQueryParamsSerializer, self).to_internal_value(normalized_data)


class QueryParamListField(serializers.ListField):
    """
    Campo gera uma lista a partir de uma string separada por virgula ou valor único.
    """

    def to_internal_value(self, data: list[str] | str) -> Any:
        if isinstance(data, str):
            data = [part.strip() for part in data.split(",")]
        return super(QueryParamListField, self).to_internal_value(data)


class PeriodInputSerializer(serializers.Serializer):
    """
    Campos para filtrar um período de tempo. \n
    Campos de entrada: init_datetime, end_datetime

    """

    init_datetime = serializers.DateTimeField(help_text="Data e hora de início")
    end_datetime = serializers.DateTimeField(help_text="Data e hora de término")

    def validate(self, data: dict) -> dict:
        if data["init_datetime"] > data["end_datetime"]:
            raise serializers.ValidationError(
                "A data de início não pode ser maior que a data de término"
            )
        return data
