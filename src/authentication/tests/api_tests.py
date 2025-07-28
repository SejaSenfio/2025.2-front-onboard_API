import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from authentication.models import UserTeamChoice
from authentication.tests.factories import UserFactory


@pytest.mark.django_db
def test_registro_e_login():
    client = APIClient()
    email = "novo@senfio.com"
    password = "SenhaS3nf100!"

    resp = client.post(
        reverse("register"),
        {
            "email": email,
            "password": password,
            "team": UserTeamChoice.ENGENHARIA,
            "works_since": "2023-01-01",
        },
        content_type="application/json",
    )
    assert resp.status_code == 201

    login = client.post(
        reverse("token_obtain_pair"),
        {"email": email, "password": password},
        content_type="application/json",
    )
    assert login.status_code == 200
    assert "access" in login.data


@pytest.mark.django_db
def test_me_endpoint_returns_user_data():
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(reverse("me"))
    assert response.status_code == 200
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_password_change_success():
    user = UserFactory()
    user.set_password("senhaAntiga123")
    user.save()

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.patch(
        reverse("change_password"),
        {"current_password": "senhaAntiga123", "new_password": "NovaSenha456!"},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert "alterada" in response.data["detail"]


@pytest.mark.django_db
def test_password_change_fails_with_wrong_current():
    user = UserFactory()
    user.set_password("senhaCerta")
    user.save()

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.patch(
        reverse("change_password"),
        {"current_password": "senhaErrada", "new_password": "NovaSenhaSegura!"},
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "incorreta" in response.data["detail"]


@pytest.mark.django_db
def test_logout_blacklists_refresh_token():
    from rest_framework_simplejwt.tokens import RefreshToken

    user = UserFactory()
    refresh = RefreshToken.for_user(user)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        reverse("token_logout"), {"refresh": str(refresh)}, content_type="application/json"
    )
    assert response.status_code == 205
    assert "Logout realizado" in response.data["detail"]
