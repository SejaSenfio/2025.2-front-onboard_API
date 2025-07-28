from django.urls import path

from .views import (
    ChangePasswordView,
    ListUsersView,
    LoginView,
    LogoutView,
    MeView,
    RefreshTokenView,
    RegisterView,
)

urlpatterns = [
    # Auth
    path("/login", LoginView.as_view(), name="token_obtain_pair"),
    path("/refresh", RefreshTokenView.as_view(), name="token_refresh"),
    path("/logout", LogoutView.as_view(), name="token_logout"),
    path("/register", RegisterView.as_view(), name="register"),
    path("/me", MeView.as_view(), name="me"),
    path("/change-password", ChangePasswordView.as_view(), name="change_password"),
    path("/users", ListUsersView.as_view(), name="list_users"),
]
