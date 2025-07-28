from datetime import timedelta

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .base import BACKEND_APP_VERSION


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_prefix="JWT_")
    # ---------------------------------------------------------------------------#
    SIGNING_KEY: str = Field(default="your-secret-key-CHANGEME")


JWT_SETTINGS = JWTSettings()


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "api.pagination.StandardPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "api.filters.FieldSearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "EXCEPTION_HANDLER": "shared.api.exception_handler.api_exceptions",
    ## FORMATTING
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S-03:00",
    "DATE_FORMAT": "%Y-%m-%d",
    "TIME_FORMAT": "%H:%M:%S",
    "DATETIME_INPUT_FORMATS": ["%Y-%m-%dT%H:%M:%S-03:00"],
    "DATE_INPUT_FORMATS": ["%Y-%m-%d"],
    "TIME_INPUT_FORMATS": ["%H:%M:%S"],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS384",
    "SIGNING_KEY": JWT_SETTINGS.SIGNING_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}


SPECTACULAR_SETTINGS = {
    "TITLE": "API Onboard - Backend",
    "DESCRIPTION": """
    Documentação de endpoints do projeto '[Challenge] - Backend' da Senfio.

    ==> Parâmetros gerais de consulta:
    - `page`: Página a ser retornada.
    - `page_size`: Quantidade de itens por página.
    - `ordering`: Campo a ser ordenado. (prefixo '-' para ordem decrescente)
    - `search`: Campo a ser pesquisado. \n \
        Por padrão a pesquisa é feita com o operador "icontains" (case-insensitive e parcial). \n \
        Para pesquisas mais complexas: \n \
            -> Buscando num campo específico : `?search=field::value`.
            -> Buscando em vários campos específicos : `?search=field1::value1;field2::value2`.
            -> Buscando com operadores avançados: (&field__lookup=value) | (?search=field__lookup::value) \n \
                Lookup         | Descrição
                ---------------|--------------------------------
                exact          | Busca um valor exato (case-sensitive).
                iexact         | Busca exata, mas case-insensitive.
                contains       | Verifica se contém um valor (case-sensitive).
                icontains      | Verifica se contém um valor (case-insensitive).
                startswith     | Começa com (case-sensitive).
                istartswith    | Começa com (case-insensitive).
                endswith       | Termina com (case-sensitive).
                iendswith      | Termina com (case-insensitive).
                gt             | Maior que. | .filter(age__gt=18)
                gte            | Maior ou igual a.
                lt             | Menor que.
                lte            | Menor ou igual a.
    """,
    "VERSION": BACKEND_APP_VERSION,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
