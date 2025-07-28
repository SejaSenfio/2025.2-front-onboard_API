from typing import Any

from django.core.exceptions import PermissionDenied
from django.db.models.manager import BaseManager
from drf_spectacular.utils import extend_schema_view
from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.api.doc import ApiDoc
from shared.api.serializers import GenericResponseSerializer

from .models import Coupon, Redemption
from .serializers import (
    CouponSerializer,
    CreateRedemptionSerializer,
    RedemptionSerializer,
)


@extend_schema_view(
    get=ApiDoc(
        op="list_coupons",
        tag="Coupons",
        title="Listar Cupons",
        desc="Lista todos os cupons disponíveis.",
        responses={200: CouponSerializer(many=True)},
    ),
    post=ApiDoc(
        op="create_coupon",
        tag="Coupons",
        title="Criar Cupom",
        desc="Cria um novo cupom.",
        body_payload=CouponSerializer,
        responses={201: GenericResponseSerializer},
    ),
)
class CouponListCreateView(generics.ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer: Any) -> None:
        if not self.request.user.is_staff:
            raise PermissionDenied("Apenas administradores podem criar cupons.")
        serializer.save()


@extend_schema_view(
    get=ApiDoc(
        op="retrieve_update_delete_coupon",
        tag="Coupons",
        title="Detalhes do Cupom",
        desc="Obtém, atualiza ou remove um cupom específico.",
        responses={200: CouponSerializer},
    ),
    put=ApiDoc(
        op="update_coupon",
        tag="Coupons",
        title="Atualizar Cupom",
        desc="Atualiza os detalhes de um cupom existente.",
        body_payload=CouponSerializer,
        responses={200: GenericResponseSerializer},
    ),
    patch=ApiDoc(
        op="partial_update_coupon",
        tag="Coupons",
        title="Atualizar Parcialmente Cupom",
        desc="Atualiza parcialmente os detalhes de um cupom existente.",
        body_payload=CouponSerializer,
        responses={200: GenericResponseSerializer},
    ),
    delete=ApiDoc(
        op="delete_coupon",
        tag="Coupons",
        title="Remover Cupom",
        desc="Remove um cupom existente.",
        responses={204: GenericResponseSerializer},
    ),
)
class CouponDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer: Any) -> None:
        if not self.request.user.is_staff:
            raise PermissionDenied("Apenas administradores podem editar cupons.")
        serializer.save()

    def perform_destroy(self, instance: Any) -> None:
        if not self.request.user.is_staff:
            raise PermissionDenied("Apenas administradores podem remover cupons.")
        instance.delete()


@extend_schema_view(
    get=ApiDoc(
        op="list_redemptions",
        tag="Redemptions",
        title="Listar Resgates",
        desc="Lista todos os resgates feitos pelo usuário autenticado.",
        responses={200: RedemptionSerializer(many=True)},
    ),
    post=ApiDoc(
        op="create_redemption",
        tag="Redemptions",
        title="Criar Resgate",
        desc="Cria um novo resgate para o cupom especificado.",
        body_payload=CreateRedemptionSerializer,
        responses={201: GenericResponseSerializer},
    ),
)
class RedemptionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> BaseManager[Redemption]:
        return Redemption.objects.filter(user=self.request.user).select_related("coupon")

    def get_serializer_class(self) -> type[CreateRedemptionSerializer]:
        if self.request.method == "POST":
            return CreateRedemptionSerializer
        return RedemptionSerializer

    def perform_create(self, serializer: Any) -> None:
        serializer.save(user=self.request.user)


@extend_schema_view(
    get=ApiDoc(
        op="retrieve_delete_redemption",
        tag="Redemptions",
        title="Detalhes do Resgate",
        desc="Obtém ou remove um resgate específico.",
        responses={200: RedemptionSerializer},
    ),
    delete=ApiDoc(
        op="delete_redemption",
        tag="Redemptions",
        title="Remover Resgate",
        desc="Remove um resgate específico.",
        responses={204: GenericResponseSerializer},
    )
)
class RedemptionDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RedemptionSerializer

    def get_queryset(self) -> BaseManager[Redemption]:
        return Redemption.objects.filter(user=self.request.user).select_related("coupon")



@extend_schema_view(
    get=ApiDoc(
        op="get_balance",
        tag="Coupons",
        title="Saldo de Cupons",
        desc="Obtém o saldo de cupons disponíveis para o usuário autenticado.",
        responses={200: CouponSerializer(many=True)},
    )
)
class BalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user
        data = []
        for coupon in Coupon.objects.filter(available=True):
            resgates = Redemption.objects.filter(user=user, coupon=coupon).count()
            saldo = None
            if coupon.max_redemptions is None:
                saldo = 0 if resgates >= 1 else 1
            else:
                saldo = max(0, coupon.max_redemptions - resgates)
            data.append({"coupon": CouponSerializer(coupon).data, "remaining": saldo})
        return Response(data)


@extend_schema_view(
    get=ApiDoc(
        op="recent_redemptions",
        tag="Redemptions",
        title="Resgates Recentes",
        desc="Lista os últimos resgates feitos.",
        responses={200: RedemptionSerializer(many=True)},
    )
)
class RecentRedemptionsView(APIView):
    def get(self, request: Request) -> Response:
        recent = Redemption.objects.select_related("coupon").order_by("-redeemed_at")[:20]
        output = RedemptionSerializer(recent, many=True).data
        return Response(output)
