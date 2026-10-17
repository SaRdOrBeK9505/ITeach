"""
Django settings for ITeach project.
"""

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-me-in-production")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*").split(",")


# ─── APPLICATIONS ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Jazzmin must be BEFORE django.contrib.admin
    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",
    "django_filters",
    "drf_yasg",

    # Local
    "accounts.apps.AccountsConfig",
    "students.apps.StudentsConfig",
    "dashboard.apps.DashboardConfig",
    "landing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",          # CORS – must be high
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "iteach.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "iteach.wsgi.application"


# ─── DATABASE ─────────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ─── PASSWORD VALIDATION ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ─── INTERNATIONALIZATION ──────────────────────────────────────────────────────
LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True


# ─── STATIC & MEDIA ───────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ─── DEFAULT PK & AUTH USER MODEL ─────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"



# ─── DJANGO REST FRAMEWORK ────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# ─── SIMPLE JWT ──────────────────────────────────────────────────────────────
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_HEADER_TYPES": ("Bearer", "JWT"),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}


# ─── CORS & CSRF ──────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=True, cast=bool)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://iteachh.vercel.app",
    "https://admin-pi-two-47.vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://iteachh.vercel.app",
    "https://admin-pi-two-47.vercel.app",
    "https://*.pythonanywhere.com",
]


# ─── SWAGGER / drf-yasg ───────────────────────────────────────────────────────
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        },
        "Basic": {"type": "basic"},
        "Session": {"type": "apiKey", "in": "cookie", "name": "sessionid"},
    },
    "USE_SESSION_AUTH": True,
    "LOGIN_URL": "/admin/login/",
    "LOGOUT_URL": "/admin/logout/",
    "DOC_EXPANSION": "none",       # Collapsed by default – cleaner
    "DEEP_LINKING": True,
    "SHOW_EXTENSIONS": True,
    "DEFAULT_MODEL_RENDERING": "example",
    "DEFAULT_AUTO_SCHEMA_CLASS": "iteach.swagger.AutoMultipartSchema",
}

REDOC_SETTINGS = {
    "LAZY_RENDERING": False,
}


# ─── JAZZMIN ─────────────────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "ITeach Admin",
    "site_header": "ITeach",
    "site_brand": "ITeach",
    "site_logo": None,
    "site_logo_classes": "img-circle",
    "welcome_sign": "ITeach Admin Paneliga xush kelibsiz",
    "copyright": "ITeach O'quv Markazi",
    "search_model": ["landing.Course", "landing.Mentor", "landing.Application"],
    "topmenu_links": [
        {"name": "Bosh sahifa", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "API Docs", "url": "/api/docs/", "new_window": True},
        {"name": "Sayt", "url": "https://iteachh.vercel.app", "new_window": True},
    ],
    "usermenu_links": [
        {"name": "Profil", "url": "admin:auth_user_change", "icon": "fas fa-user"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "landing",
        "landing.SiteSettings",
        "landing.HeroSection",
        "landing.Statistic",
        "landing.AboutSection",
        "landing.Course",
        "landing.CourseCategory",
        "landing.Mentor",
        "landing.Partner",
        "landing.Graduate",
        "landing.Testimonial",
        "landing.FAQ",
        "landing.BlogPost",
        "landing.BlogCategory",
        "landing.Application",
        "landing.ContactMessage",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "landing.SiteSettings": "fas fa-cog",
        "landing.HeroSection": "fas fa-star",
        "landing.Statistic": "fas fa-chart-bar",
        "landing.Course": "fas fa-graduation-cap",
        "landing.CourseCategory": "fas fa-tags",
        "landing.CourseFeature": "fas fa-check-circle",
        "landing.Mentor": "fas fa-chalkboard-teacher",
        "landing.Partner": "fas fa-handshake",
        "landing.Graduate": "fas fa-award",
        "landing.FAQ": "fas fa-question-circle",
        "landing.BlogPost": "fas fa-blog",
        "landing.BlogCategory": "fas fa-folder",
        "landing.Application": "fas fa-file-alt",
        "landing.ContactMessage": "fas fa-envelope",
        "landing.AboutSection": "fas fa-info-circle",
        "landing.Testimonial": "fas fa-comments",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-success",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
}
