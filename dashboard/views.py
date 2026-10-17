from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils import timezone
from datetime import timedelta

from students.models import Student
from students.serializers import StudentListSerializer
from landing.models import Course, Mentor, StudentResult, Application, ContactMessage
from landing.serializers import CourseListSerializer, ApplicationAdminSerializer


class DashboardSummaryView(APIView):
    """
    GET /api/admin/dashboard/
    Main executive dashboard KPI metrics and recent tables for iTeach administrator portal.
    Corresponds exactly to screenshots image copy.png and image copy 2.png.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        ctx = {"request": request}

        # 1. Metric counts
        total_courses = Course.objects.filter(is_active=True).count()
        total_students = Student.objects.filter(status="Faol").count()
        total_mentors = Mentor.objects.filter(is_active=True).count()
        total_results = StudentResult.objects.filter(is_active=True).count()
        total_applications = Application.objects.count()
        new_applications = Application.objects.filter(status="new").count()
        unread_contacts = ContactMessage.objects.filter(is_read=False).count()

        # 2. Recent Students (as shown in image copy.png)
        recent_students = Student.objects.select_related("course").order_by("-created_at")[:10]

        # 3. Courses overview (as shown in image copy 2.png)
        courses = Course.objects.select_related("category", "mentor").filter(is_active=True).order_by("order")[:10]

        # 4. Recent Applications
        recent_applications = Application.objects.select_related("course").order_by("-created_at")[:10]

        return Response({
            "metrics": {
                "courses": {
                    "label": "Jami kurslar",
                    "value": total_courses,
                    "growth": "+0%",
                },
                "students": {
                    "label": "O'quvchilar",
                    "value": total_students,
                    "growth": "+0%",
                },
                "mentors": {
                    "label": "Mentorlar",
                    "value": total_mentors,
                    "growth": "+0%",
                },
                "results": {
                    "label": "Natijalar",
                    "value": total_results,
                    "growth": "+0%",
                },
                "applications": {
                    "label": "Arizalar",
                    "value": total_applications,
                    "new_count": new_applications,
                },
                "unread_messages": {
                    "label": "O'qilmagan xabarlar",
                    "value": unread_contacts,
                }
            },
            "recent_students": StudentListSerializer(recent_students, many=True, context=ctx).data,
            "courses": CourseListSerializer(courses, many=True, context=ctx).data,
            "recent_applications": ApplicationAdminSerializer(recent_applications, many=True, context=ctx).data,
        }, status=status.HTTP_200_OK)


class DashboardAnalyticsView(APIView):
    """
    GET /api/admin/dashboard/analytics/
    Provides charts and analytics for student distribution per course and monthly trends.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Course distribution
        courses = Course.objects.filter(is_active=True).values("id", "name")
        distribution = []
        for c in courses:
            count = Student.objects.filter(course_id=c["id"]).count()
            distribution.append({
                "course_id": c["id"],
                "course_name": c["name"],
                "students_count": count
            })

        # Applications status breakdown
        app_stats = {
            "new": Application.objects.filter(status="new").count(),
            "called": Application.objects.filter(status="called").count(),
            "enrolled": Application.objects.filter(status="enrolled").count(),
            "rejected": Application.objects.filter(status="rejected").count(),
        }

        return Response({
            "course_distribution": distribution,
            "applications_breakdown": app_stats,
        }, status=status.HTTP_200_OK)
