from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Student
from .serializers import StudentListSerializer, StudentDetailSerializer


class StudentListCreateView(generics.ListCreateAPIView):
    """
    GET /api/admin/students/  – List all students with search, filters and ordering.
    POST /api/admin/students/ – Create a new student.
    """
    queryset = Student.objects.select_related("course").all()
    serializer_class = StudentDetailSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "course"]
    search_fields = ["full_name", "phone", "email", "lesson_time", "notes"]
    ordering_fields = ["created_at", "full_name", "enrolled_date", "status"]
    ordering = ["-created_at"]
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return StudentDetailSerializer
        return StudentListSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/admin/students/<id>/    – Retrieve student details.
    PUT/PATCH /api/admin/students/<id>/ – Update student.
    DELETE /api/admin/students/<id>/ – Delete student.
    """
    queryset = Student.objects.select_related("course").all()
    serializer_class = StudentDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
