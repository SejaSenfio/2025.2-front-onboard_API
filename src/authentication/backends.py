import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpRequest


class AuthenticationBackend(ModelBackend):
    def user_can_authenticate(self, user: models.Model) -> bool:
        """
        Rejeita usuários com 'is_active' = False.
        """
        return getattr(user, "is_active", True)

    def authenticate(
        self,
        request: HttpRequest,
        username: str | None = None,
        password: str | None = None,
        **kwargs: dict,
    ) -> None | AbstractUser:
        logging.debug(
            f"Autenticação de usuário iniciada. Dados fornecidos: U: {username}, P: {password} kwargs: {kwargs}."
        )
        User = get_user_model()

        # Definir username a partir de kwargs, se não fornecido diretamente
        if username is None:
            username = kwargs.get(str(User.USERNAME_FIELD), "")  # type: ignore

        # Retornar se username ou senha não forem fornecidos
        if not username or not password:
            logging.debug("Email ou senha não foram fornecidos.")
            return None

        try:
            logging.debug(f"Procurando usuário pelo e-mail: {username}")
            user = User.objects.get(email=username)
            logging.debug(f"Usuário encontrado: {user}")
        except User.DoesNotExist:
            logging.debug(f"Usuário com e-mail '{username}' não existe.")
            return None

        # Verificar se o usuário está inativo
        if not user.is_active:
            logging.debug("Tentativa de autenticação em conta inativa.")
            return None

        # Verificar a senha
        if user.check_password(password):
            logging.debug("Autenticação realizada com sucesso!")
            return user
        else:
            logging.debug("Senha incorreta.")
            return None

    def get_user(self, user_id: int) -> AbstractUser | None:
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
