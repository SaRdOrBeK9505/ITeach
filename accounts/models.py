from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model for iTeach platform.
    Supports role-based access: Super Admin, Admin, Mentor, Student.
    """
    ROLE_CHOICES = [
        ("superadmin", _("Bosh Administrator")),
        ("admin", _("Administrator")),
        ("mentor", _("Mentor / O'qituvchi")),
        ("student", _("O'quvchi")),
    ]

    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Telefon raqam"))
    avatar = models.ImageField(upload_to="users/avatars/", null=True, blank=True, verbose_name=_("Avatar / Rasm"))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="admin", verbose_name=_("Rol"))
    bio = models.TextField(blank=True, verbose_name=_("Biografiya"))

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
