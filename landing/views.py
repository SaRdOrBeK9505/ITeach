from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    SiteSettings, HeroSection, HeroSlide, Statistic,
    CourseCategory, Course, CourseFeature,
    Mentor, Partner, Graduate,
    FAQ, BlogCategory, BlogPost,
    Application, ContactMessage,
    AboutSection, AboutFeature, Testimonial,
    StudentResult, LearningProcess,
)
from .serializers import (
    SiteSettingsSerializer,
    HeroSectionSerializer, HeroSlideSerializer,
    StatisticSerializer,
    CourseCategorySerializer,
    CourseListSerializer, CourseDetailSerializer, CourseWriteSerializer,
    CourseFeatureSerializer,
    MentorListSerializer, MentorDetailSerializer, MentorWriteSerializer,
    PartnerSerializer,
    GraduateListSerializer, GraduateWriteSerializer,
    FAQSerializer,
    BlogCategorySerializer,
    BlogPostListSerializer, BlogPostDetailSerializer, BlogPostWriteSerializer,
    ApplicationSerializer, ApplicationAdminSerializer,
    ContactMessageSerializer, ContactMessageAdminSerializer,
    AboutSectionSerializer, AboutSectionWriteSerializer,
    AboutFeatureSerializer,
    TestimonialListSerializer, TestimonialWriteSerializer,
    StudentResultSerializer, LearningProcessSerializer,
)


# ─────────────────────────────────────────────
# SITE SETTINGS  (singleton – always return first record)
# ─────────────────────────────────────────────
class SiteSettingsView(APIView):
    """GET /api/settings/ – Return site-wide settings."""
    permission_classes = [AllowAny]

    def get(self, request):
        obj = SiteSettings.objects.first()
        if not obj:
            return Response({}, status=status.HTTP_200_OK)
        serializer = SiteSettingsSerializer(obj, context={"request": request})
        return Response(serializer.data)


class SiteSettingsUpdateView(generics.RetrieveUpdateAPIView):
    """GET/PUT/PATCH /api/admin/settings/ – Admin update."""
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return obj


# ─────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────
class HeroSectionView(APIView):
    """GET /api/hero/ – Active hero section."""
    permission_classes = [AllowAny]

    def get(self, request):
        obj = HeroSection.objects.filter(is_active=True).first()
        if not obj:
            return Response({}, status=status.HTTP_200_OK)
        serializer = HeroSectionSerializer(obj, context={"request": request})
        return Response(serializer.data)


class HeroSectionAdminListCreate(generics.ListCreateAPIView):
    """GET/POST /api/admin/hero/"""
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer
    permission_classes = [IsAdminUser]


class HeroSectionAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /api/admin/hero/<pk>/"""
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer
    permission_classes = [IsAdminUser]


# ─────────────────────────────────────────────
# STATISTICS
# ─────────────────────────────────────────────
class StatisticListView(generics.ListAPIView):
    """GET /api/statistics/ – Active stats."""
    queryset = Statistic.objects.filter(is_active=True)
    serializer_class = StatisticSerializer
    permission_classes = [AllowAny]


class StatisticAdminListCreate(generics.ListCreateAPIView):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer
    permission_classes = [IsAdminUser]


class StatisticAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer
    permission_classes = [IsAdminUser]


# ─────────────────────────────────────────────
# COURSE CATEGORIES
# ─────────────────────────────────────────────
class CourseCategoryListView(generics.ListAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [AllowAny]


class CourseCategoryAdminListCreate(generics.ListCreateAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [IsAdminUser]


class CourseCategoryAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [IsAdminUser]


# ─────────────────────────────────────────────
# COURSES
# ─────────────────────────────────────────────
class CourseListView(generics.ListAPIView):
    """GET /api/courses/ – Public course listing (N+1 prevented via select_related)."""
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "level", "is_popular", "is_active"]
    search_fields = ["name", "short_description"]
    ordering_fields = ["order", "name", "price"]

    def get_queryset(self):
        return (
            Course.objects.filter(is_active=True)
            .select_related("category")
            .order_by("order", "name")
        )


class CourseDetailView(generics.RetrieveAPIView):
    """GET /api/courses/<slug>/ – Full course detail with features & mentors."""
    serializer_class = CourseDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Course.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related("features", "mentors")
        )


class CourseAdminListCreate(generics.ListCreateAPIView):
    """GET/POST /api/admin/courses/"""
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "level", "is_popular", "is_active"]
    search_fields = ["name"]

    def get_queryset(self):
        return Course.objects.select_related("category").prefetch_related("features").all()

    def get_serializer_class(self):
        return CourseWriteSerializer if self.request.method == "POST" else CourseListSerializer


class CourseAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /api/admin/courses/<pk>/"""
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Course.objects.select_related("category").prefetch_related("features", "mentors").all()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return CourseWriteSerializer
        return CourseDetailSerializer


# ─────────────────────────────────────────────
# COURSE FEATURES (nested under course)
# ─────────────────────────────────────────────
class CourseFeatureAdminListCreate(generics.ListCreateAPIView):
    serializer_class = CourseFeatureSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CourseFeature.objects.none()
        return CourseFeature.objects.filter(course_id=self.kwargs["course_pk"])

    def perform_create(self, serializer):
        course = Course.objects.get(pk=self.kwargs["course_pk"])
        serializer.save(course=course)


class CourseFeatureAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseFeatureSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CourseFeature.objects.none()
        return CourseFeature.objects.filter(course_id=self.kwargs["course_pk"])


# ─────────────────────────────────────────────
# MENTORS
# ─────────────────────────────────────────────
class MentorListView(generics.ListAPIView):
    """GET /api/mentors/ – Active mentors."""
    serializer_class = MentorListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Mentor.objects.filter(is_active=True).order_by("order", "name")


class MentorDetailView(generics.RetrieveAPIView):
    """GET /api/mentors/<pk>/"""
    serializer_class = MentorDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Mentor.objects.filter(is_active=True).prefetch_related("courses")


class MentorAdminListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ["name", "position"]

    def get_queryset(self):
        return Mentor.objects.prefetch_related("courses").all()

    def get_serializer_class(self):
        return MentorWriteSerializer if self.request.method == "POST" else MentorListSerializer


class MentorAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Mentor.objects.prefetch_related("courses").all()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return MentorWriteSerializer
        return MentorDetailSerializer


# ─────────────────────────────────────────────
# PARTNERS
# ─────────────────────────────────────────────
class PartnerListView(generics.ListAPIView):
    queryset = Partner.objects.filter(is_active=True)
    serializer_class = PartnerSerializer
    permission_classes = [AllowAny]


class PartnerAdminListCreate(generics.ListCreateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [IsAdminUser]


class PartnerAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [IsAdminUser]


# ─────────────────────────────────────────────
# GRADUATES
# ─────────────────────────────────────────────
class GraduateListView(generics.ListAPIView):
    serializer_class = GraduateListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course"]

    def get_queryset(self):
        return Graduate.objects.filter(is_active=True).select_related("course").order_by("order")


class GraduateAdminListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Graduate.objects.select_related("course").all()

    def get_serializer_class(self):
        return GraduateWriteSerializer if self.request.method == "POST" else GraduateListSerializer


class GraduateAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Graduate.objects.select_related("course").all()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return GraduateWriteSerializer
        return GraduateListSerializer


# ─────────────────────────────────────────────
# FAQ
# ─────────────────────────────────────────────
class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]


class FAQAdminListCreate(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAdminUser]


class FAQAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAdminUser]


# ─────────────────────────────────────────────
# BLOG
# ─────────────────────────────────────────────
class BlogCategoryListView(generics.ListAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [AllowAny]


class BlogPostListView(generics.ListAPIView):
    """GET /api/blog/ – Published posts only."""
    serializer_class = BlogPostListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category"]
    search_fields = ["title", "excerpt"]

    def get_queryset(self):
        return (
            BlogPost.objects.filter(is_published=True)
            .select_related("category", "author")
            .order_by("-published_at")
        )


class BlogPostDetailView(generics.RetrieveAPIView):
    """GET /api/blog/<slug>/ – Increment view count on access."""
    serializer_class = BlogPostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).select_related("category", "author")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views atomically
        BlogPost.objects.filter(pk=instance.pk).update(views_count=instance.views_count + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogCategoryAdminListCreate(generics.ListCreateAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAdminUser]


class BlogCategoryAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAdminUser]


class BlogPostAdminListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category", "is_published"]
    search_fields = ["title"]

    def get_queryset(self):
        return BlogPost.objects.select_related("category", "author").all()

    def get_serializer_class(self):
        return BlogPostWriteSerializer if self.request.method == "POST" else BlogPostListSerializer

    def perform_create(self, serializer):
        # Auto-set published_at when publishing
        data = serializer.validated_data
        if data.get("is_published") and not data.get("published_at"):
            serializer.save(published_at=timezone.now())
        else:
            serializer.save()


class BlogPostAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return BlogPost.objects.select_related("category", "author").all()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return BlogPostWriteSerializer
        return BlogPostDetailSerializer

    def perform_update(self, serializer):
        data = serializer.validated_data
        if data.get("is_published") and not self.get_object().published_at:
            serializer.save(published_at=timezone.now())
        else:
            serializer.save()


# ─────────────────────────────────────────────
# APPLICATION (Lead form)
# ─────────────────────────────────────────────
class ApplicationCreateView(generics.CreateAPIView):
    """POST /api/apply/ – Public: submit an enrollment application."""
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [AllowAny]


class ApplicationAdminListView(generics.ListAPIView):
    """GET /api/admin/applications/ – Admin: list all applications."""
    serializer_class = ApplicationAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "course"]
    search_fields = ["full_name", "phone"]
    ordering_fields = ["created_at", "status"]

    def get_queryset(self):
        return Application.objects.select_related("course").all()


class ApplicationAdminDetail(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/admin/applications/<pk>/ – Admin: update status/notes."""
    serializer_class = ApplicationAdminSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Application.objects.select_related("course").all()


class ApplicationConvertToStudentView(APIView):
    """
    POST /api/admin/applications/<pk>/convert-to-student/
    Directly converts a lead / application into an active enrolled Student in the CRM.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        from students.models import Student
        app = generics.get_object_or_404(Application, pk=pk)
        student = Student.objects.create(
            full_name=app.full_name,
            phone=app.phone,
            course=app.course,
            status="Faol",
            notes=f"Arizadan yaratildi (#{app.id}): {app.message or app.notes}",
        )
        app.status = "enrolled"
        app.save()
        return Response({
            "detail": "Ariza muvaffaqiyatli o'quvchiga aylantirildi.",
            "student_id": student.id,
            "student_name": student.full_name,
        }, status=status.HTTP_201_CREATED)



# ─────────────────────────────────────────────
# CONTACT MESSAGE
# ─────────────────────────────────────────────
class ContactMessageCreateView(generics.CreateAPIView):
    """POST /api/contact/ – Public: send a contact message."""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]


class ContactMessageAdminListView(generics.ListAPIView):
    serializer_class = ContactMessageAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["is_read"]
    search_fields = ["full_name", "email", "subject"]

    def get_queryset(self):
        return ContactMessage.objects.all()


class ContactMessageAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageAdminSerializer
    permission_classes = [IsAdminUser]


# ─────────────────────────────────────────────
# ABOUT SECTION
# ─────────────────────────────────────────────
class AboutSectionView(APIView):
    """GET /api/about/ – Active about section."""
    permission_classes = [AllowAny]

    def get(self, request):
        obj = AboutSection.objects.filter(is_active=True).prefetch_related("features").first()
        if not obj:
            return Response({}, status=status.HTTP_200_OK)
        serializer = AboutSectionSerializer(obj, context={"request": request})
        return Response(serializer.data)


class AboutSectionAdminListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return AboutSection.objects.prefetch_related("features").all()

    def get_serializer_class(self):
        return AboutSectionWriteSerializer if self.request.method == "POST" else AboutSectionSerializer


class AboutSectionAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return AboutSection.objects.prefetch_related("features").all()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return AboutSectionWriteSerializer
        return AboutSectionSerializer


# ─────────────────────────────────────────────
# TESTIMONIALS
# ─────────────────────────────────────────────
class TestimonialListView(generics.ListAPIView):
    serializer_class = TestimonialListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course"]

    def get_queryset(self):
        return Testimonial.objects.filter(is_active=True).select_related("course").order_by("order")


class TestimonialAdminListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Testimonial.objects.select_related("course").all()

    def get_serializer_class(self):
        return TestimonialWriteSerializer if self.request.method == "POST" else TestimonialListSerializer


class TestimonialAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Testimonial.objects.select_related("course").all()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return TestimonialWriteSerializer
        return TestimonialListSerializer


# ─────────────────────────────────────────────
# HERO SLIDES
# ─────────────────────────────────────────────
class HeroSlideListView(generics.ListAPIView):
    """GET /api/hero-slides/"""
    queryset = HeroSlide.objects.filter(is_active=True)
    serializer_class = HeroSlideSerializer
    permission_classes = [AllowAny]


class HeroSlideAdminListCreate(generics.ListCreateAPIView):
    """GET/POST /api/admin/hero-slides/"""
    queryset = HeroSlide.objects.all()
    serializer_class = HeroSlideSerializer
    permission_classes = [IsAdminUser]


class HeroSlideAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /api/admin/hero-slides/<pk>/"""
    queryset = HeroSlide.objects.all()
    serializer_class = HeroSlideSerializer
    permission_classes = [IsAdminUser]


# ─────────────────────────────────────────────
# STUDENT RESULTS (Video Reels)
# ─────────────────────────────────────────────
class StudentResultListView(generics.ListAPIView):
    """GET /api/results/"""
    queryset = StudentResult.objects.filter(is_active=True)
    serializer_class = StudentResultSerializer
    permission_classes = [AllowAny]


class StudentResultAdminListCreate(generics.ListCreateAPIView):
    """GET/POST /api/admin/results/"""
    queryset = StudentResult.objects.all()
    serializer_class = StudentResultSerializer
    permission_classes = [IsAdminUser]


class StudentResultAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /api/admin/results/<pk>/"""
    queryset = StudentResult.objects.all()
    serializer_class = StudentResultSerializer
    permission_classes = [IsAdminUser]


# ─────────────────────────────────────────────
# LEARNING PROCESS (Ta'lim qanday amalga oshiriladi?)
# ─────────────────────────────────────────────
class LearningProcessListView(generics.ListAPIView):
    """GET /api/learning-process/"""
    queryset = LearningProcess.objects.filter(is_active=True)
    serializer_class = LearningProcessSerializer
    permission_classes = [AllowAny]


class LearningProcessAdminListCreate(generics.ListCreateAPIView):
    """GET/POST /api/admin/learning-process/"""
    queryset = LearningProcess.objects.all()
    serializer_class = LearningProcessSerializer
    permission_classes = [IsAdminUser]


class LearningProcessAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /api/admin/learning-process/<pk>/"""
    queryset = LearningProcess.objects.all()
    serializer_class = LearningProcessSerializer
    permission_classes = [IsAdminUser]


# ─────────────────────────────────────────────
# LANDING PAGE  –  all-in-one endpoint
# ─────────────────────────────────────────────
class LandingPageView(APIView):
    """
    GET /api/landing/
    Returns ALL data needed to render the full landing page in a single request.
    Avoids N+1 by using select_related / prefetch_related everywhere.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Settings
        settings = SiteSettings.objects.first()
        # Hero with slides
        hero = HeroSection.objects.filter(is_active=True).prefetch_related("slides").first()
        hero_slides = list(HeroSlide.objects.filter(is_active=True).order_by("order"))
        # Stats
        stats = list(Statistic.objects.filter(is_active=True).order_by("order"))
        # About
        about = AboutSection.objects.filter(is_active=True).prefetch_related("features").first()
        # Courses
        courses = list(
            Course.objects.filter(is_active=True)
            .select_related("category", "mentor")
            .prefetch_related("features", "mentors")
            .order_by("order")
        )
        # Mentors
        mentors = list(Mentor.objects.filter(is_active=True).order_by("order"))
        # Student Results / Reels
        results = list(StudentResult.objects.filter(is_active=True).order_by("order"))
        # Learning Process
        learning_process = list(LearningProcess.objects.filter(is_active=True).order_by("order"))
        # Partners
        partners = list(Partner.objects.filter(is_active=True).order_by("order"))
        # Graduates
        graduates = list(
            Graduate.objects.filter(is_active=True).select_related("course").order_by("order")
        )
        # Testimonials
        testimonials = list(
            Testimonial.objects.filter(is_active=True).select_related("course").order_by("order")
        )
        # FAQ
        faqs = list(FAQ.objects.filter(is_active=True).order_by("order"))
        # Blog (latest 3)
        blog_posts = list(
            BlogPost.objects.filter(is_published=True)
            .select_related("category", "author")
            .order_by("-published_at")[:3]
        )

        ctx = {"request": request}
        return Response({
            "settings": SiteSettingsSerializer(settings, context=ctx).data if settings else {},
            "hero": HeroSectionSerializer(hero, context=ctx).data if hero else {},
            "hero_slides": HeroSlideSerializer(hero_slides, many=True, context=ctx).data,
            "statistics": StatisticSerializer(stats, many=True, context=ctx).data,
            "about": AboutSectionSerializer(about, context=ctx).data if about else {},
            "courses": CourseListSerializer(courses, many=True, context=ctx).data,
            "student_results": StudentResultSerializer(results, many=True, context=ctx).data,
            "results": StudentResultSerializer(results, many=True, context=ctx).data,
            "learning_process": LearningProcessSerializer(learning_process, many=True, context=ctx).data,
            "mentors": MentorListSerializer(mentors, many=True, context=ctx).data,
            "partners": PartnerSerializer(partners, many=True, context=ctx).data,
            "graduates": GraduateListSerializer(graduates, many=True, context=ctx).data,
            "testimonials": TestimonialListSerializer(testimonials, many=True, context=ctx).data,
            "faqs": FAQSerializer(faqs, many=True, context=ctx).data,
            "latest_posts": BlogPostListSerializer(blog_posts, many=True, context=ctx).data,
        })
