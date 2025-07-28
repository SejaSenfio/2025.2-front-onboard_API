from rest_framework import serializers

from authentication.serializers import UserSerializer

from .models import Coupon, Redemption

# ---------------------
# COUPON SERIALIZER
# ---------------------


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["id", "code", "description", "max_redemptions", "available", "created_at"]
        read_only_fields = ["id", "created_at"]


# ---------------------
# REDEMPTION SERIALIZER
# ---------------------


class RedemptionSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Redemption
        fields = ["id", "coupon", "redeemed_at", "user"]


class CreateRedemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redemption
        fields = ["coupon"]

    def validate(self, data: dict) -> dict:
        user = self.context["request"].user
        coupon = data["coupon"]
        redemption = Redemption(user=user, coupon=coupon)
        redemption.clean()  # Chama a lógica do model
        return data

    def create(self, validated_data: dict) -> Redemption:
        user = self.context["request"].user
        validated_data["user"] = user
        return Redemption.objects.create(**validated_data)
