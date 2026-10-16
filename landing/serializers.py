from rest_framework import serializers
from .models import (
    SiteSettings, HeroSection, HeroSlide, Statistic,
    CourseCategory, Course, CourseFeature,
    Mentor, Partner, Graduate,
    FAQ, BlogCategory, BlogPost,
    Application, ContactMessage,
    AboutSection, AboutFeature, Testimonial,
    StudentResult, LearningProcess,
)


# ─────────────────────────────────────────────
# SITE SETTINGS
# ─────────────────────────────────────────────
class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"


# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
class HeroSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSlide
        fields = "__all__"


class HeroSectionSerializer(serializers.ModelSerializer):
    slides = HeroSlideSerializer(many=True, read_only=True)

    class Meta:
        model = HeroSection
        fields = "__all__"


# ─────────────────────────────────────────────
# STATISTICS
# ─────────────────────────────────────────────
class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = "__all__"


# ─────────────────────────────────────────────
# COURSES
# ─────────────────────────────────────────────
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = "__all__"


class CourseFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFeature
        exclude = ["course"]


class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing courses (fully compatible with frontend)."""
    title = serializers.CharField(source="name", read_only=True)
    students = serializers.IntegerField(source="students_count", read_only=True)
    mentor = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "name", "title", "slug", "short_description", "image", "icon",
            "duration_months", "level", "price", "old_price",
            "status", "course_format", "students", "students_count",
            "mentor", "is_popular", "order", "category", "category_name",
        ]

    def get_mentor(self, obj):
        if obj.mentor:
            return obj.mentor.name
        first_m = obj.mentors.first()
        return first_m.name if first_m else ""


class CourseDetailSerializer(serializers.ModelSerializer):
    """Full serializer with nested features and mentors (read-only)."""
    category = CourseCategorySerializer(read_only=True)
    features = CourseFeatureSerializer(many=True, read_only=True)
    mentors = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_mentors(self, obj):
        # Select only needed fields to avoid over-fetching
        return obj.mentors.filter(is_active=True).values(
            "id", "name", "position", "photo", "experience_years"
        )


class CourseWriteSerializer(serializers.ModelSerializer):
    """Writable serializer for create/update operations."""
    class Meta:
        model = Course
        fields = "__all__"


# ─────────────────────────────────────────────
# MENTORS
# ─────────────────────────────────────────────
class MentorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = [
            "id", "name", "position", "photo", "experience_years",
            "telegram", "linkedin", "instagram", "github", "order",
        ]


class MentorDetailSerializer(serializers.ModelSerializer):
    courses = CourseListSerializer(many=True, read_only=True)

    class Meta:
        model = Mentor
        fields = "__all__"


class MentorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = "__all__"


# ─────────────────────────────────────────────
# PARTNERS
# ─────────────────────────────────────────────
class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = "__all__"


# ─────────────────────────────────────────────
# GRADUATES
# ─────────────────────────────────────────────
class GraduateListSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Graduate
        fields = [
            "id", "name", "photo", "company", "position",
            "salary", "testimonial", "order", "course", "course_name",
        ]


class GraduateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduate
        fields = "__all__"


# ─────────────────────────────────────────────
# FAQ
# ─────────────────────────────────────────────
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


# ─────────────────────────────────────────────
# BLOG
# ─────────────────────────────────────────────
class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = "__all__"


class BlogPostListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id", "title", "slug", "excerpt", "cover_image",
            "author", "author_name", "category", "category_name",
            "is_published", "published_at", "views_count",
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    author = MentorListSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = "__all__"


class BlogPostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"


# ─────────────────────────────────────────────
# APPLICATION (Lead)
# ─────────────────────────────────────────────
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["status", "notes", "created_at", "updated_at"]


class ApplicationAdminSerializer(serializers.ModelSerializer):
    """Full serializer for admin – includes status and notes."""
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Application
        fields = "__all__"


# ─────────────────────────────────────────────
# CONTACT MESSAGE
# ─────────────────────────────────────────────
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = ["is_read", "created_at", "updated_at"]


class ContactMessageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"


# ─────────────────────────────────────────────
# ABOUT SECTION
# ─────────────────────────────────────────────
class AboutFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutFeature
        exclude = ["about"]


class AboutSectionSerializer(serializers.ModelSerializer):
    features = AboutFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = AboutSection
        fields = "__all__"


class AboutSectionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = "__all__"


# ─────────────────────────────────────────────
# TESTIMONIALS
# ─────────────────────────────────────────────
class TestimonialListSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Testimonial
        fields = [
            "id", "name", "photo", "rating", "text",
            "order", "course", "course_name",
        ]


class TestimonialWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"


# ─────────────────────────────────────────────
# STUDENT RESULTS (Video reels)
# ─────────────────────────────────────────────
class StudentResultSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = StudentResult
        fields = [
            "id", "name", "tag", "video_url", "video_file", "src",
            "thumbnail", "instagram_url", "order", "is_active", "created_at"
        ]

    def get_src(self, obj):
        if obj.video_url:
            return obj.video_url
        if obj.video_file:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.video_file.url) if request else obj.video_file.url
        return ""


# ─────────────────────────────────────────────
# LEARNING PROCESS (Ta'lim qanday amalga oshiriladi?)
# ─────────────────────────────────────────────
class LearningProcessSerializer(serializers.ModelSerializer):
    number = serializers.CharField(source="step_number", read_only=True)

    class Meta:
        model = LearningProcess
        fields = ["id", "step_number", "number", "title", "description", "icon", "order", "is_active"]

