from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "course", "lesson_time", "status", "enrolled_date")
    list_editable = ("status", "lesson_time")
    list_filter = ("status", "course", "enrolled_date")
    search_fields = ("full_name", "phone", "email", "lesson_time", "notes")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("O'quvchi ma'lumotlari", {"fields": ("full_name", "phone", "email", "avatar")}),
        ("Ta'lim", {"fields": ("course", "lesson_time", "status", "enrolled_date")}),
        ("Qo'shimcha", {"fields": ("notes", "created_at", "updated_at")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("course")
