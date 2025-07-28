import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from authentication.models import User
from authentication.tests.factories import UserFactory


@pytest.mark.django_db
def test_email_invalido():
    user = User(email="teste@gmail.com", team="RH", works_since=timezone.now().date())
    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.django_db
def test_user_creation_with_factory():
    user = UserFactory()
    assert user.email.endswith("@senfio.com")
    assert user.works_since <= timezone.now().date()
