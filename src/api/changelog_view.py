import re
from pathlib import Path

from drf_spectacular.utils import OpenApiExample, extend_schema_view, inline_serializer
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from config.settings import BASE_DIR
from shared.api.doc import ApiDoc

CHANGELOG_FILE_PATH = str(Path(BASE_DIR) / "../docs/CHANGELOG.md")


@extend_schema_view(
    get=ApiDoc(
        op="get_changelog",
        tag="Changelog",
        title="Changelog",
        desc="Recupera o changelog do projeto.",
        responses={
            200: inline_serializer(
                "ChangelogResponse",
                {
                    "version": serializers.CharField(),
                    "released": serializers.DateField(),
                    "features": serializers.ListField(
                        child=serializers.CharField(), allow_empty=True
                    ),
                    "bugfixes": serializers.ListField(
                        child=serializers.CharField(), allow_empty=True
                    ),
                },
            )
        },
        examples=[
            OpenApiExample(
                name="Changelog",
                response_only=True,
                value=[
                    {
                        "version": "0.2.0",
                        "released": "2023-11-01",
                        "features": [
                            "Introduzida funcionalidade A.",
                            "Atualização da biblioteca B.",
                        ],
                        "bugfixes": ["Resolvido bug C.", "Aprimorado suporte a D."],
                    },
                    {
                        "version": "0.1.0",
                        "released": "2023-10-01",
                        "features": [
                            "Adicionada nova funcionalidade X.",
                            "Melhorias na interface do usuário.",
                        ],
                        "bugfixes": ["Corrigido erro Y.", "Ajustado problema de desempenho Z."],
                    },
                ],
            )
        ],
    )
)
class ChangelogAPIView(GenericAPIView):
    serializer_class = serializers.Serializer

    def get(self, request: Request) -> Response:
        changelogs: dict = {}
        current_version = None
        current_section = None

        for line in Path(CHANGELOG_FILE_PATH).read_text(encoding="utf-8").splitlines():
            version_match = re.match(r"^#\s+(\d+\.\d+\.\d+)\s+\((\d{4}-\d{2}-\d{2})\)", line)
            section_match = re.match(r"^###\s+(.*)", line)
            bullet_match = re.match(r"^- (.+)", line)

            if version_match:
                current_version, released = version_match.groups()
                changelogs[current_version] = {
                    "released": released,
                    "features": [],
                    "bugfixes": [],
                }
            elif section_match:
                section = section_match.group(1).lower()
                if "feature" in section:
                    current_section = "features"
                elif "bug" in section:
                    current_section = "bugfixes"
                else:
                    current_section = None
            elif bullet_match and current_version:
                if current_section is None:
                    continue
                entry = bullet_match.group(1)
                changelogs[current_version][current_section].append(entry)

        output_changelog = []

        for version, data in changelogs.items():
            output_changelog.append(
                {
                    "version": version,
                    "released": data["released"],
                    "features": data["features"],
                    "bugfixes": data["bugfixes"],
                }
            )

        return Response(output_changelog)
