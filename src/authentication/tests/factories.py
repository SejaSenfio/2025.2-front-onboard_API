import random
from datetime import timedelta

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from faker import Faker
from unidecode import unidecode

from authentication.models import User, UserTeamChoice

fake = Faker("pt_BR")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(
        lambda _: f"{unidecode(fake.first_name().split()[0].lower())}.{unidecode(fake.last_name().split()[-1].lower())}@senfio.com"
    )
    team = factory.LazyAttribute(
        lambda _: random.choice([choice[0] for choice in UserTeamChoice.choices])
    )
    works_since = timezone.now().date() - timedelta(days=365)
    password = factory.PostGenerationMethodCall("set_password", "SenhaS3nf10")
    is_staff = factory.Faker("boolean", chance_of_getting_true=40)
