from rest_framework import serializers
from .models import Student
from landing.models import Course


class StudentListSerializer(serializers.ModelSerializer):
    """
    Serializer optimized for table view (as shown in admin screenshot image copy 4.png).
    Includes course name, badges, and formatted date.
    """
    course_name = serializers.CharField(source="course.name", read_only=True, default="")
    course_format = serializers.CharField(source="course.course_format", read_only=True, default="")
    role = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id", "full_name", "role", "phone", "email", "avatar",
            "course", "course_name", "course_format",
            "lesson_time", "status", "notes",
            "enrolled_date", "created_at", "updated_at",
        ]

    def get_role(self, obj):
        return "O'quvchi"


class StudentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with course info and write capabilities."""
    course_name = serializers.CharField(source="course.name", read_only=True, default="")

    class Meta:
        model = Student
        fields = "__all__"

    def validate_phone(self, value):
        # Clean phone numbers
        cleaned = value.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if len(cleaned) < 9:
            raise serializers.ValidationError("Telefon raqami kamida 9 ta raqamdan iborat bo'lishi kerak.")
        return value
