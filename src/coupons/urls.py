from django.urls import path

from .views import (
    BalanceView,
    CouponDetailView,
    CouponListCreateView,
    RecentRedemptionsView,
    RedemptionDetailView,
    RedemptionListCreateView,
)

urlpatterns = [
    path("/balance", BalanceView.as_view(), name="balance"),
    path("/recent-redemptions", RecentRedemptionsView.as_view(), name="recent_redemptions"),
    path(
        "/redemptions",
        RedemptionListCreateView.as_view(),
        name="redemption-list-create",
    ),
    path(
        "/redemptions/<int:pk>",
        RedemptionDetailView.as_view(),
        name="redemption-detail",
    ),
    path(
        "",
        CouponListCreateView.as_view(),
        name="coupon-list-create",
    ),
    path(
        "/<int:pk>",
        CouponDetailView.as_view(),
        name="coupon-detail",
    ),
]
