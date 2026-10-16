from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AdminLoginSerializer(serializers.Serializer):
    """
    Authenticates administrator by username OR email and returns JWT tokens.
    Designed specifically for the iTeach admin portal login screen.
    """
    login = serializers.CharField(
        required=True,
        help_text=_("Foydalanuvchi nomi yoki email manzili")
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )
    remember_me = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        login_input = attrs.get("login", "").strip()
        password = attrs.get("password")

        # Resolve user by username or email
        user = None
        if "@" in login_input:
            user_obj = User.objects.filter(email__iexact=login_input).first()
            if user_obj:
                user = authenticate(username=user_obj.username, password=password)
        else:
            user = authenticate(username=login_input, password=password)

        if not user:
            raise serializers.ValidationError(
                _("Login yoki parol noto'g'ri kiritildi.")
            )

        if not user.is_active:
            raise serializers.ValidationError(
                _("Foydalanuvchi hisobi faol emas.")
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)

        role = "Super Admin" if user.is_superuser else ("Administrator" if user.is_staff else "Foydalanuvchi")

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.get_full_name() or user.username,
                "role": role,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            }
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """Profile serializer for current logged in user."""
    full_name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "full_name", "role", "is_staff", "is_superuser", "date_joined",
        ]
        read_only_fields = ["id", "username", "role", "is_staff", "is_superuser", "date_joined"]

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

    def get_role(self, obj):
        return "Super Admin" if obj.is_superuser else ("Administrator" if obj.is_staff else "Foydalanuvchi")


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change endpoint."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Eski parol noto'g'ri."))
        return value
