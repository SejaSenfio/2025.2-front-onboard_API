from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from ..changelog_view import ChangelogAPIView

urlpatterns = [
    path("changelog", ChangelogAPIView.as_view(), name="changelog-api"),
    path(
        "doc", SpectacularSwaggerView.as_view(url_name="endp-api-doc-schema"), name="endp-api-doc"
    ),
    path("schema", SpectacularAPIView.as_view(), name="endp-api-doc-schema"),
    path("authentication", include("authentication.urls")),
    path("coupons", include("coupons.urls")),
]
