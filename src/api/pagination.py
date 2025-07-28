from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 1000

    def paginate_queryset(self, queryset: Any, request: Any, view: Any | None = None) -> None | Any:
        """
        Se `page_size=0` for enviado na query string, retorna todos os dados sem paginação.
        """
        page_size = request.query_params.get(self.page_size_query_param)
        if page_size == "0":
            return None

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data: list) -> Response:
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "next_page": self.page.number + 1 if self.page.has_next() else None,
                "previous_page": self.page.number - 1 if self.page.has_previous() else None,
                "page_size": self.get_page_size(self.request),
                "results": data,
            }
        )

    def get_paginated_response_schema(self, schema: Any) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["count", "results"],
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 123,
                },
                "total_pages": {"type": "integer", "example": 4},
                "current_page": {"type": "integer", "example": 1},
                "next_page": {"type": "integer", "nullable": True, "example": 2},
                "previous_page": {"type": "integer", "nullable": True, "example": None},
                "page_size": {"type": "integer", "example": 25},
                "results": schema,
            },
        }
