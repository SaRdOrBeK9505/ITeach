from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Student(models.Model):
    STATUS_CHOICES = [
        ("Faol", _("Faol")),
        ("Nofaol", _("Nofaol")),
        ("Bitirgan", _("Bitirgan")),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_profile",
        verbose_name=_("Foydalanuvchi hisobi"),
    )
    full_name = models.CharField(max_length=150, verbose_name=_("Ism Familiya"))
    phone = models.CharField(max_length=20, verbose_name=_("Telefon raqam"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    avatar = models.ImageField(upload_to="students/", null=True, blank=True, verbose_name=_("Avatar / Rasm"))
    course = models.ForeignKey(
        "landing.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enrolled_students",
        verbose_name=_("Kurs"),
    )
    lesson_time = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Dars vaqti"),
        help_text=_("Masalan: ertt, 14:00, Dush-Chor-Jum 18:00"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Faol", verbose_name=_("Holat"))
    notes = models.TextField(blank=True, verbose_name=_("Admin izohi"))
    enrolled_date = models.DateField(auto_now_add=True, verbose_name=_("Ro'yxatdan o'tgan sana"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan vaqt"))

    class Meta:
        verbose_name = _("O'quvchi")
        verbose_name_plural = _("O'quvchilar")
        ordering = ["-created_at"]

    def __str__(self):
        course_name = self.course.name if self.course else "Kurs biriktirilmagan"
        return f"{self.full_name} - {course_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically synchronize students count on the course
        if self.course_id:
            active_count = Student.objects.filter(course_id=self.course_id, status="Faol").count()
            self.course.__class__.objects.filter(id=self.course_id).update(students_count=active_count)

    def delete(self, *args, **kwargs):
        course_id = self.course_id
        res = super().delete(*args, **kwargs)
        if course_id:
            from landing.models import Course
            active_count = Student.objects.filter(course_id=course_id, status="Faol").count()
            Course.objects.filter(id=course_id).update(students_count=active_count)
        return res
