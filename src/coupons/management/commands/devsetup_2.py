from django.core.management.base import BaseCommand

from config.settings import DJANGO_SETT
from coupons.tests.factories import CouponFactory, coupons_options


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

        for coupon_option in coupons_options:
            coupon = CouponFactory(
                code=coupon_option[0],
                description=coupon_option[1],
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Cupom {coupon.code} criado com sucesso! Disponível: {'SIM' if coupon.available else 'NÃO'}"
                )
            )
