import logging
import pprint
from typing import Any, Callable

from drf_spectacular.utils import F, OpenApiExample, OpenApiResponse, extend_schema
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from shared.api.serializers import ApiErrorSerializer as _ApiErrorSerializer
from shared.api.serializers import (
    OrderingListApiViewSerializer as _OrderingListApiViewSerializer,
)
from shared.api.serializers import (
    SearchListApiViewSerializer as _SearchListApiViewSerializer,
)


def log_request_data(data: str | dict) -> None:
    if isinstance(data, dict):
        logging.debug(f"Request data: {pprint.pformat(data)}")
    else:
        logging.debug(f"Request data: {data}")


class ApiDoc(PydanticBaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")
    # -----------------------------------
    op: str
    tag: str
    title: str
    desc: str
    query_params: Any | list = Field(default=None, description="Query params para o endpoint.")
    body_payload: Any = Field(default=None, description="Body payload para o endpoint.")
    responses: dict = Field(default_factory=dict, description="Responses for the endpoint.")
    examples: list[OpenApiExample] = Field(
        default_factory=list, description="Examples for the endpoint."
    )
    search_fields: list[str] = Field(
        default_factory=list, description="Campos de busca para o endpoint."
    )
    ordering_fields: list[str] = Field(
        default_factory=list, description="Campos de ordenação para o endpoint."
    )
    no_auth: bool = Field(
        default=False,
        description="Se True, não requer autenticação para acessar o endpoint.",
    )

    def generate(self) -> Callable[[F], F]:
        parameters = []
        if isinstance(self.query_params, list):
            parameters.extend([qp for qp in self.query_params if qp])
        elif self.query_params is not None:
            parameters.append(self.query_params)

        if self.search_fields:
            parameters.append(
                _SearchListApiViewSerializer(data={"search_fields": self.search_fields})
            )
        if self.ordering_fields:
            parameters.append(
                _OrderingListApiViewSerializer(data={"ordering_fields": self.ordering_fields}),
            )

        schema_args: dict = dict(
            operation_id=self.op,
            tags=[self.tag],
            summary=self.title,
            description=self.desc,
            responses={**self.responses, **DEFAULT_SCHEMA_RESPONSES},
            examples=self.examples,
        )

        if self.body_payload:
            schema_args["request"] = self.body_payload
        if parameters:
            schema_args["parameters"] = parameters
        if self.no_auth:
            schema_args["auth"] = []

        return extend_schema(**schema_args)

    def __new__(cls, *args: list, **kwargs: dict) -> Callable[[F], F]:  # type: ignore
        instance = super().__new__(cls)  # Cria a instância do modelo
        cls.__init__(instance, *args, **kwargs)  # Inicializa o modelo
        return instance.generate()  # Retorna o resultado de generate


DEFAULT_SCHEMA_RESPONSES = {
    400: _ApiErrorSerializer,
    401: OpenApiResponse(
        description="Usuário não autenticado.",
        response=_ApiErrorSerializer,
        examples=[
            OpenApiExample(
                name="not_authenticated",
                media_type="application/json",
                value={
                    "code": "not_authenticated",
                    "message": "Usuário não autenticado.",
                },
            )
        ],
    ),
    403: OpenApiResponse(
        description="Permissão negada para o recurso solicitado.",
        response=_ApiErrorSerializer,
        examples=[
            OpenApiExample(
                name="permission_denied",
                media_type="application/json",
                value={
                    "code": "permission_denied",
                    "message": "Permissão negada para o recurso solicitado.",
                },
            )
        ],
    ),
    404: OpenApiResponse(
        description="Recurso procurado não encontrado.",
        response=_ApiErrorSerializer,
        examples=[
            OpenApiExample(
                name="not_found",
                media_type="application/json",
                value={
                    "code": "not_found",
                    "message": "Recurso procurado não encontrado.",
                },
            )
        ],
    ),
    409: OpenApiResponse(
        description="Um conflito ocorreu durante a solicitação.",
        response=_ApiErrorSerializer,
        examples=[
            OpenApiExample(
                name="conflict",
                media_type="application/json",
                value={
                    "code": "conflict",
                    "message": "Um conflito ocorreu durante a solicitação.",
                },
            )
        ],
    ),
    417: OpenApiResponse(
        description="Expectativa não atendida.",
        response=_ApiErrorSerializer,
        examples=[
            OpenApiExample(
                name="expectation_failed",
                media_type="application/json",
                value={
                    "code": "expectation_failed",
                    "message": "Expectativa não atendida.",
                },
            )
        ],
    ),
    500: OpenApiResponse(
        description="Erro interno do servidor.",
        response=_ApiErrorSerializer,
        examples=[
            OpenApiExample(
                name="server_error",
                media_type="application/json",
                value={
                    "code": "server_error",
                    "message": "Erro interno do servidor.",
                },
            )
        ],
    ),
    501: OpenApiResponse(
        description="Recurso solicitado ainda não foi implementado.",
        response=_ApiErrorSerializer,
        examples=[
            OpenApiExample(
                name="not_implemented",
                media_type="application/json",
                value={
                    "code": "not_implemented",
                    "message": "Recurso solicitado ainda não foi implementado.",
                },
            )
        ],
    ),
}
