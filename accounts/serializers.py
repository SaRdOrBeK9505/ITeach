from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    SimpleJWT TokenObtainPairSerializer vorisi.
    Administratorlar va xodimlar uchun JWT access va refresh token yaratadi.
    Token payload va response tarkibida foydalanuvchining roli (role) ham birga yuboriladi.
    """
    login = serializers.CharField(required=False, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            self.fields["username"].required = False

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # JWT token payload ichiga custom claimlar:
        token["role"] = user.role
        token["username"] = user.username
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser
        return token

    def validate(self, attrs):
        # Foydalanuvchi login yoki username orqali kirishini ta'minlash
        login_val = (attrs.get("login") or attrs.get(self.username_field) or "").strip()
        if not login_val:
            raise serializers.ValidationError({"username": [_("Foydalanuvchi nomi yoki email kiritilishi shart.")]})

        # Agar email kiritilgan bo'lsa, mos keluvchi username ni aniqlash
        if "@" in login_val:
            user_obj = User.objects.filter(email__iexact=login_val).first()
            if user_obj:
                attrs[self.username_field] = user_obj.username
            else:
                attrs[self.username_field] = login_val
        else:
            attrs[self.username_field] = login_val

        data = super().validate(attrs)

        # Response ichida tokenlar bilan birga user va uning roli yuboriladi
        data["role"] = self.user.role
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "full_name": self.user.get_full_name() or self.user.username,
            "role": self.user.role,
            "role_display": self.user.get_role_display(),
            "phone": self.user.phone,
            "avatar": self.user.avatar.url if self.user.avatar else None,
            "is_staff": self.user.is_staff,
            "is_superuser": self.user.is_superuser,
        }
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    SimpleJWT TokenRefreshSerializer vorisi.
    Refresh token orqali yangi access token beradi va
    response ichida foydalanuvchi roli (role) ni ham qaytaradi.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        try:
            refresh = RefreshToken(attrs["refresh"])
            user_id = refresh.payload.get("user_id")
            if user_id:
                user = User.objects.filter(id=user_id).first()
                if user:
                    data["role"] = user.role
        except Exception:
            pass
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Profile serializer for current logged in user."""
    full_name = serializers.SerializerMethodField()
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "full_name", "phone", "avatar", "role", "role_display",
            "is_staff", "is_superuser", "date_joined",
        ]
        read_only_fields = ["id", "username", "role", "role_display", "is_staff", "is_superuser", "date_joined"]

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change endpoint."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Eski parol noto'g'ri."))
        return value
