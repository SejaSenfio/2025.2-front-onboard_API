import logging

from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from shared.api.doc import ApiDoc
from shared.api.serializers import GenericResponseSerializer

from .models import User
from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserLogoutSerializer,
    UserSerializer,
)


@extend_schema_view(
    post=ApiDoc(
        op="login",
        tag="Auth/Users",
        title="Login",
        desc="Loga o usuário no sistema.",
        body_payload=LoginSerializer,
        responses={200: TokenObtainPairSerializer},
        no_auth=True,
    )
)
class LoginView(TokenObtainPairView):
    permission_classes: tuple = ()
    authentication_classes: tuple = ()


@extend_schema_view(
    post=ApiDoc(
        op="refresh_token",
        tag="Auth/Users",
        title="Atualizar token",
        desc="Atualiza o token de acesso.",
        body_payload=TokenRefreshSerializer,
        responses={200: TokenRefreshSerializer},
        no_auth=True,
    )
)
class RefreshTokenView(TokenRefreshView):
    permission_classes: tuple = ()
    authentication_classes: tuple = ()


@extend_schema_view(
    post=ApiDoc(
        op="logout",
        tag="Auth/Users",
        title="Logout",
        desc="Desloga o usuário.",
        body_payload=UserLogoutSerializer,
        responses={205: GenericResponseSerializer},
    )
)
class LogoutView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            token = RefreshToken(data["refresh"])
            token.blacklist()
        except TokenError as e:
            logging.info(f"Token já foi invalidado ou não é válido: {e}")

        out_serializer = GenericResponseSerializer(data={"detail": "Logout realizado com sucesso."})
        out_serializer.is_valid(raise_exception=True)
        return Response(out_serializer.validated_data, status=status.HTTP_205_RESET_CONTENT)


@extend_schema_view(
    post=ApiDoc(
        op="register",
        tag="Auth/Users",
        title="Registrar usuário",
        desc="Registra um novo usuário no sistema.",
        body_payload=RegisterSerializer,
        responses={201: UserSerializer},
        no_auth=True,
    )
)
class RegisterView(APIView):
    permission_classes: tuple = ()

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=201)


@extend_schema_view(
    get=ApiDoc(
        op="me",
        tag="Auth/Users",
        title="Quem sou eu",
        desc="Retorna os dados do usuário autenticado.",
        responses={200: UserSerializer},
    )
)
class MeView(APIView):
    def get(self, request: Request) -> Response:
        return Response(UserSerializer(request.user).data)


@extend_schema_view(
    patch=ApiDoc(
        op="change_password",
        tag="Auth/Users",
        title="Alterar senha",
        desc="Altera a senha do usuário autenticado.",
        body_payload=ChangePasswordSerializer,
        responses={200: GenericResponseSerializer},
    )
)
class ChangePasswordView(APIView):
    def patch(self, request: Request) -> Response:
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.check_password(serializer.validated_data["current_password"]):
            return Response({"detail": "Senha atual incorreta."}, status=400)

        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Senha alterada com sucesso."})


@extend_schema_view(
    post=ApiDoc(
        op="verify_token",
        tag="Auth/Users",
        title="Verificar token",
        desc="Verifica se o token é válido.",
        body_payload=TokenVerifySerializer,
        responses={200: None},
        no_auth=True,
    )
)
class UserTokenVerifyView(TokenVerifyView):
    permission_classes: tuple = ()
    authentication_classes: tuple = tuple()

    def post(self, request: Request) -> Response:
        return super(UserTokenVerifyView, self).post(request)


@extend_schema_view(
    get=ApiDoc(
        op="list_users",
        tag="Auth/Users",
        title="Listar usuários",
        desc="Lista todos os usuários do sistema.",
        search_fields=["email", "team"],
        responses={200: UserSerializer(many=True)},
    )
)
class ListUsersView(ListAPIView):
    """
    View para listar usuários.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ["email", "team"]
