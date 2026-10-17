from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    AdminTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)

User = get_user_model()


class AdminTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/login/ yoki POST /api/auth/token/
    SimpleJWT asosida administratorlarga JWT access va refresh token beradi
    hamda foydalanuvchining roli (role) va ma'lumotlarini qaytaradi.
    """
    serializer_class = AdminTokenObtainPairSerializer




class CustomTokenRefreshView(TokenRefreshView):
    """
    POST /api/auth/refresh/ yoki POST /api/auth/token/refresh/
    SimpleJWT asosida tokenni yangilaydi va foydalanuvchi rolini (role) qaytaradi.
    """
    serializer_class = CustomTokenRefreshSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /api/auth/me/  – Get profile of logged in user.
    PUT/PATCH /api/auth/me/ – Update profile (first_name, last_name, email).
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """
    POST /api/auth/change-password/
    Change password for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response(
            {"detail": "Parol muvaffaqiyatli yangilandi."},
            status=status.HTTP_200_OK
        )
