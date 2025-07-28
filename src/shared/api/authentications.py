import logging
from typing import Any

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from config.settings import API_APPS_TOKENS, DJANGO_SETT


class MesosAppTagTokenScheme(OpenApiAuthenticationExtension):
    target_class = "shared.api.authentications.MesosAppTagAuthentication"
    name = "MesosAppTokenAuth"  # Nome do esquema no OpenAPI

    def get_security_definition(self, auto_schema: Any) -> dict:
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Token fixo esperado no header Authorization. Ex: Authorization: Token <mesos_token>",
        }


class MesosAppTagAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> tuple[None, None] | tuple[None, str] | None:
        if DJANGO_SETT.DEBUG:
            logging.debug("Modo debug ativo. Nenhuma autenticação aplicada.")
            return (None, None)

        if request.method in ["POST", "DELETE"]:
            token = request.headers.get("Authorization")
            if not token or token != API_APPS_TOKENS.MESOS_TOKEN:
                raise AuthenticationFailed("Token não existe ou é inválido.")

            return (None, token)
        return None


class HubsatTagTokenScheme(OpenApiAuthenticationExtension):
    target_class = "shared.api.authentications.HubsatTagEventAuthentication"
    name = "HubsatTagTokenAuth"  # Nome do esquema no OpenAPI

    def get_security_definition(self, auto_schema: Any) -> dict:
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Token fixo esperado no header Authorization. Ex: Authorization: Token <hubsat_token>",
        }


class HubsatTagEventAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> tuple[None, None] | tuple[None, str] | None:
        if DJANGO_SETT.DEBUG:
            logging.debug("Modo debug ativo. Nenhuma autenticação aplicada.")
            return (None, None)

        if request.method in ["POST"]:
            token = request.headers.get("Authorization")
            if not token or token != API_APPS_TOKENS.HUBSAT_TOKEN:
                raise AuthenticationFailed("Token não existe ou é inválido.")

            return (None, token)
        return None
