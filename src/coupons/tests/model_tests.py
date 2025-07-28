import pytest
from django.core.exceptions import ValidationError

from coupons.models import Redemption
from coupons.tests.factories import CouponFactory, RedemptionFactory, UserFactory


@pytest.mark.django_db
def test_limite_resgates():
    user = UserFactory()
    coupon = CouponFactory(max_redemptions=2, available=True)
    RedemptionFactory.create_batch(2, user=user, coupon=coupon)

    redemption = Redemption(user=user, coupon=coupon)
    with pytest.raises(ValidationError):
        redemption.clean()
