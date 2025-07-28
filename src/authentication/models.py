from datetime import date
from typing import Any, Self

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models

from shared.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str | None = None, **extra_fields: Any) -> Any:
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.clean()
        user.save()
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: Any) -> Any:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class UserTeamChoice(models.TextChoices):
    TECNOLOGIA = "TECNOLOGIA", "Tecnologia"
    MARKETING = "MARKETING", "Marketing"
    VENDAS = "VENDAS", "Vendas"
    FINANCEIRO = "FINANCEIRO", "Financeiro"
    RH = "RH", "Recursos Humanos"
    ENGENHARIA = "ENGENHARIA", "Engenharia"


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    team = models.CharField(
        max_length=100,
        choices=UserTeamChoice.choices,
        default=UserTeamChoice.TECNOLOGIA,
        verbose_name="Equipe",
    )
    works_since = models.DateField(verbose_name="Data de entrada na empresa")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    is_staff = models.BooleanField(default=False, verbose_name="Membro da equipe(Administrador)")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["team", "works_since"]

    objects = UserManager()

    @property
    def team_display(self) -> str:
        return UserTeamChoice(self.team).label if self.team else "Não especificado"

    def clean(self) -> None:
        super().clean()
        if not self.email.endswith("@senfio.com"):
            raise ValidationError("O e-mail deve ser do domínio @senfio.com.")
        if self.works_since > date.today():
            raise ValidationError("A data de entrada na empresa não pode ser futura.")

    def save(self, *args: list, **kwargs: dict) -> Self:
        self.clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["-id"]
