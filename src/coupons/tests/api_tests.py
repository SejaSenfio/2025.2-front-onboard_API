import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from coupons.tests.factories import CouponFactory, RedemptionFactory, UserFactory


@pytest.mark.django_db
def test_balance_endpoint_usage_limited_coupon():
    user = UserFactory()
    coupon = CouponFactory(max_redemptions=3)
    RedemptionFactory.create_batch(1, user=user, coupon=coupon)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(reverse("balance"))
    assert response.status_code == 200
    for c in response.data:
        if c["coupon"]["code"] == coupon.code:
            assert c["remaining"] == 2


@pytest.mark.django_db
def test_balance_endpoint_usage_unique_coupon():
    user = UserFactory()
    coupon = CouponFactory(max_redemptions=None)
    RedemptionFactory.create(user=user, coupon=coupon)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(reverse("balance"))
    assert response.status_code == 200
    for c in response.data:
        if c["coupon"]["code"] == coupon.code:
            assert c["remaining"] == 0

@pytest.mark.django_db
def test_coupon_list_authenticated():
    user = UserFactory()
    CouponFactory.create_batch(3)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(reverse("coupon-list-create"))
    assert response.status_code == 200
    assert len(response.data.get("results")) == 3


@pytest.mark.django_db
def test_coupon_create_requires_admin():
    user = UserFactory(is_staff=False)
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        reverse("coupon-list-create"),
        {"code": "TESTE01", "description": "Cupom teste", "max_redemptions": 5, "available": True},
        content_type="application/json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_coupon_create_by_admin_success():
    admin = UserFactory(is_staff=True)
    client = APIClient()
    client.force_authenticate(user=admin)

    response = client.post(
        reverse("coupon-list-create"),
        {
            "code": "ADMIN01",
            "description": "Criado por admin",
            "max_redemptions": 2,
            "available": True,
        },
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.data["code"] == "ADMIN01"


@pytest.mark.django_db
def test_coupon_detail_update_and_delete():
    admin = UserFactory(is_staff=True)
    coupon = CouponFactory()

    client = APIClient()
    client.force_authenticate(user=admin)

    url = reverse("coupon-detail", kwargs={"pk": coupon.id})

    # UPDATE
    response = client.patch(url, {"description": "Atualizado"}, content_type="application/json")
    assert response.status_code == 200
    assert response.data["description"] == "Atualizado"

    # DELETE
    response = client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_redemption_list_and_create_flow():
    user = UserFactory()
    coupon = CouponFactory(max_redemptions=3)
    RedemptionFactory(user=user, coupon=coupon)

    client = APIClient()
    client.force_authenticate(user=user)

    # Listar
    response = client.get(reverse("redemption-list-create"))
    assert response.status_code == 200
    assert len(response.data.get("results")) == 1

    # Criar outro resgate
    response = client.post(
        reverse("redemption-list-create"), {"coupon": coupon.id}, content_type="application/json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_redemption_detail_retrieve_and_delete():
    user = UserFactory()
    redemption = RedemptionFactory(user=user)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("redemption-detail", kwargs={"pk": redemption.id})

    response = client.get(url)
    assert response.status_code == 200
    assert response.data["id"] == redemption.id

    response = client.delete(url)
    assert response.status_code == 204
