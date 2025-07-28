from typing import Self

from django.core.exceptions import ValidationError
from django.db import models

from authentication.models import User
from shared.models import BaseModel


class Coupon(BaseModel):
    code = models.CharField(max_length=50, unique=True, verbose_name="Código de resgate")
    description = models.TextField(verbose_name="Descrição")
    max_redemptions = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Número máximo de resgates"
    )
    available = models.BooleanField(default=True, verbose_name="Disponível")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    def clean(self) -> None:
        super().clean()
        if self.max_redemptions is not None and self.max_redemptions == 0:
            raise ValidationError(
                "O número máximo de resgates deve ser maior que zero ou nulo (para uso único)."
            )

    def save(self, *args: list, **kwargs: dict) -> Self:
        self.clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Cupom"
        verbose_name_plural = "Cupons"
        ordering = ["-created_at"]


class Redemption(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="redemptions", verbose_name="Usuário"
    )
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name="redemptions", verbose_name="Cupom"
    )
    redeemed_at = models.DateTimeField(auto_now_add=True, verbose_name="Resgatado em")

    def clean(self) -> None:
        super().clean()
        if not self.coupon.available:
            raise ValidationError("Este cupom não está disponível para resgate.")

        resgate_count = Redemption.objects.filter(user=self.user, coupon=self.coupon).count()

        if self.coupon.max_redemptions is None and resgate_count > 0:
            raise ValidationError("Este cupom só pode ser resgatado uma vez por usuário.")
        elif (
            self.coupon.max_redemptions is not None and resgate_count >= self.coupon.max_redemptions
        ):
            raise ValidationError("Você atingiu o limite de resgates para este cupom.")

    def save(self, *args: list, **kwargs: dict) -> Self:
        self.clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Resgate"
        verbose_name_plural = "Resgates"
        ordering = ["-redeemed_at"]
        unique_together = [
            "user",
            "coupon",
            "redeemed_at",
        ]  # Permite múltiplos resgates se permitido no cupom
