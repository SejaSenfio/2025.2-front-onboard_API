from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User

# ---------------------
# USER SERIALIZER
# ---------------------


class UserSerializer(serializers.ModelSerializer):
    team = serializers.CharField(source='team_display', read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "email", "team", "works_since", "is_active", "is_staff"]
        read_only_fields = ["id", "is_active", "is_staff"]



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "team", "works_since"]

    def validate_email(self, value: str) -> str:
        if not value.endswith("@senfio.com"):
            raise serializers.ValidationError("O e-mail deve ser do domínio @senfio.com.")
        return value

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, value: str) -> str:
        validate_password(value)
        return value


# ---------------------
# LOGIN SERIALIZER
# ---------------------


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data: dict) -> dict:
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Credenciais inválidas.")
        data["user"] = user
        return data


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Token de atualização")

    def validate_refresh(self, value: str) -> str:
        return value
