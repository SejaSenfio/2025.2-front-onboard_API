from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from drf_spectacular.utils import extend_schema_view
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import status

from shared.api.doc import ApiDoc

from .settings.base import BACKEND_APP_VERSION

admin.site.site_header = f"APP - Backend - v{BACKEND_APP_VERSION}"
admin.site.index_title = "Início"
admin.site.site_title = "App"


class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Status of the application")


@extend_schema_view(
    get=ApiDoc(
        op="health_check",
        tag="Health",
        title="Health Check",
        desc="Check the health of the application.",
        responses={200: HealthCheckSerializer},
        no_auth=True,
    )
)
class HealthCheckView(GenericAPIView):
    serializer_class = HealthCheckSerializer
    permission_classes: list = []
    authentication_classes: list = []

    def get(self, request: Request) -> Response:
        serializer = HealthCheckSerializer(data={"status": "OK"})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VersionSerializer(serializers.Serializer):
    version = serializers.CharField(help_text="Version of the application")


@extend_schema_view(
    get=ApiDoc(
        op="version",
        tag="Version",
        title="Version",
        desc="Get the version of the application.",
        responses={200: VersionSerializer},
        no_auth=True,
    )
)
class VersionView(GenericAPIView):
    serializer_class = VersionSerializer
    permission_classes: list = []
    authentication_classes: list = []

    def get(self, request: Request) -> Response:
        serializer = VersionSerializer(data={"version": BACKEND_APP_VERSION})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


urlpatterns = [
    path("api/v1/", include("api.v1.urls")),
    path("admin/", admin.site.urls),
    path("", lambda request: redirect("health", permanent=True)),
    path("health", view=HealthCheckView.as_view(), name="endp-health"),
    path("version", view=VersionView.as_view(), name="endp-version"),
]
