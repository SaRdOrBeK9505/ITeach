from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # SimpleJWT Token olish va yangilash
    path("login/", views.AdminTokenObtainPairView.as_view(), name="login"),
    path("refresh/", views.CustomTokenRefreshView.as_view(), name="token-refresh"),

    # Profil va xavfsizlik
    path("me/", views.UserProfileView.as_view(), name="me"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),
]
