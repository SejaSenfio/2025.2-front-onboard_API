import random

from django.core.management.base import BaseCommand

from authentication.tests.factories import UserFactory
from config.settings import DJANGO_SETT


class Command(BaseCommand):
    help = "Executa automaticamente todos os comandos de popular banco de dados de todos os apps"

    def handle(self, *args: list, **kwargs: dict) -> None:
        if not DJANGO_SETT.DEBUG:
            self.stdout.write(
                self.style.WARNING(
                    "Este comando só pode ser executado em ambiente de desenvolvimento!"
                )
            )
            return None

        fuser = UserFactory(email="admin.rochedo@senfio.com", is_staff=True)
        self.stdout.write(
            self.style.SUCCESS(
                f"Usuário {fuser.email}, com senha: 'SenhaS3nf10' criado com sucesso! => ADMINISTRADOR!"
            )
        )
        for _ in range(random.randint(15, 25)):
            user = UserFactory()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Usuário {user.email}, com senha: 'SenhaS3nf10' criado com sucesso! {'=> ADMINISTRADOR!' if user.is_staff else ''}"
                )
            )
