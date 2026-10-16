from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ─── SWAGGER / REDOC SCHEMA ──────────────────────────────────────────────────
schema_view = get_schema_view(
    openapi.Info(
        title="ITeach API",
        default_version="v1",
        description=(
            "ITeach O'quv Markazi uchun to'liq REST API.\n\n"
            "**Public endpointlar** – autentifikatsiya talab qilinmaydi.\n"
            "**Admin endpointlar** – faqat `is_staff=True` foydalanuvchilar uchun."
        ),
        terms_of_service="https://iteachh.vercel.app",
        contact=openapi.Contact(email="info@iteach.uz"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # API endpoints (Modular architecture)
    path("api/auth/", include("accounts.urls", namespace="accounts")),
    path("api/admin/dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("api/admin/students/", include("students.urls", namespace="students-admin")),
    path("api/students/", include("students.urls", namespace="students")),
    path("api/", include("landing.urls", namespace="landing")),

    # Swagger UI
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # ReDoc
    path(
        "api/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    # Raw schema (JSON)
    path(
        "api/schema.json",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
