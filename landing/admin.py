from django.contrib import admin
from django.utils.html import format_html
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
# INLINES
# ─────────────────────────────────────────────
class CourseFeatureInline(admin.TabularInline):
    model = CourseFeature
    extra = 1
    fields = ("text", "order")


class HeroSlideInline(admin.TabularInline):
    model = HeroSlide
    extra = 1
    fields = ("title", "subtitle", "icon", "image", "order", "is_active")


class AboutFeatureInline(admin.TabularInline):
    model = AboutFeature
    extra = 1
    fields = ("icon", "title", "description", "order")


# ─────────────────────────────────────────────
# SITE SETTINGS  (singleton)
# ─────────────────────────────────────────────
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Asosiy", {"fields": ("site_name", "logo", "favicon")}),
        ("Aloqa", {"fields": ("phone", "phone_secondary", "email", "address", "working_hours")}),
        ("Ijtimoiy tarmoqlar", {"fields": ("telegram", "instagram", "youtube", "facebook", "tiktok", "linkedin")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
        ("Xarita", {"fields": ("map_embed_url",)}),
    )
    list_display = ("site_name", "phone", "email", "updated_at")

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


# ─────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────
@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "badge_text", "is_active", "updated_at")
    list_editable = ("is_active",)
    search_fields = ("title",)
    inlines = [HeroSlideInline]
    fieldsets = (
        ("Kontent", {"fields": ("badge_text", "title", "subtitle")}),
        ("Tugmalar", {"fields": ("primary_btn_text", "primary_btn_link", "secondary_btn_text", "secondary_btn_link")}),
        ("Rasmlar", {"fields": ("hero_image", "background_image")}),
        ("Sozlamalar", {"fields": ("is_active",)}),
    )


# ─────────────────────────────────────────────
# STATISTICS
# ─────────────────────────────────────────────
@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)


# ─────────────────────────────────────────────
# COURSES
# ─────────────────────────────────────────────
@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "mentor", "status", "course_format",
        "students_count", "price", "is_popular", "is_active", "order"
    )
    list_editable = ("status", "students_count", "is_popular", "is_active", "order")
    list_filter = ("status", "course_format", "category", "level", "is_popular", "is_active")
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CourseFeatureInline]
    fieldsets = (
        ("Asosiy", {"fields": ("name", "slug", "category", "mentor", "image", "icon")}),
        ("Tavsif", {"fields": ("short_description", "description")}),
        ("Ma'lumotlar", {"fields": ("duration_months", "level", "status", "course_format", "students_count", "price", "old_price")}),
        ("Sozlamalar", {"fields": ("is_popular", "is_active", "order")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category", "mentor")


# ─────────────────────────────────────────────
# MENTORS
# ─────────────────────────────────────────────
@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "experience_years", "is_active", "order", "photo_preview")
    list_editable = ("is_active", "order")
    search_fields = ("name", "position")
    list_filter = ("is_active",)
    filter_horizontal = ("courses",)
    fieldsets = (
        ("Shaxsiy", {"fields": ("name", "position", "photo", "experience_years", "bio")}),
        ("Kurslar", {"fields": ("courses",)}),
        ("Ijtimoiy", {"fields": ("telegram", "linkedin", "instagram", "github")}),
        ("Sozlamalar", {"fields": ("is_active", "order")}),
    )

    @admin.display(description="Rasm")
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:40px;border-radius:50%;"/>', obj.photo.url)
        return "-"


# ─────────────────────────────────────────────
# PARTNERS
# ─────────────────────────────────────────────
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "is_active", "order", "logo_preview")
    list_editable = ("is_active", "order")
    search_fields = ("name",)

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:36px;object-fit:contain;"/>', obj.logo.url)
        return "-"


# ─────────────────────────────────────────────
# GRADUATES
# ─────────────────────────────────────────────
@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "position", "course", "salary", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active", "course")
    search_fields = ("name", "company", "position")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("course")


# ─────────────────────────────────────────────
# FAQ
# ─────────────────────────────────────────────
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("question",)


# ─────────────────────────────────────────────
# BLOG
# ─────────────────────────────────────────────
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "is_published", "published_at", "views_count")
    list_editable = ("is_published",)
    list_filter = ("is_published", "category")
    search_fields = ("title", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    fieldsets = (
        ("Asosiy", {"fields": ("title", "slug", "category", "author")}),
        ("Kontent", {"fields": ("excerpt", "content", "cover_image")}),
        ("Nashr", {"fields": ("is_published", "published_at")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category", "author")


# ─────────────────────────────────────────────
# APPLICATIONS
# ─────────────────────────────────────────────
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "direction", "course", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "direction", "course")
    search_fields = ("full_name", "phone", "direction")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Ariza", {"fields": ("full_name", "phone", "direction", "course", "message")}),
        ("Holat", {"fields": ("status", "notes")}),
        ("Vaqt", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("course")


# ─────────────────────────────────────────────
# CONTACT MESSAGES
# ─────────────────────────────────────────────
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "subject", "is_read", "created_at")
    list_editable = ("is_read",)
    list_filter = ("is_read",)
    search_fields = ("full_name", "email", "subject")
    readonly_fields = ("created_at",)


# ─────────────────────────────────────────────
# ABOUT SECTION
# ─────────────────────────────────────────────
@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    list_editable = ("is_active",)
    inlines = [AboutFeatureInline]


# ─────────────────────────────────────────────
# TESTIMONIALS
# ─────────────────────────────────────────────
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "rating", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active", "rating", "course")
    search_fields = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("course")


# ─────────────────────────────────────────────
# STUDENT RESULTS (Video Reels)
# ─────────────────────────────────────────────
@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ("name", "tag", "video_url", "instagram_url", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "tag")


# ─────────────────────────────────────────────
# LEARNING PROCESS (Ta'lim qanday amalga oshiriladi?)
# ─────────────────────────────────────────────
@admin.register(LearningProcess)
class LearningProcessAdmin(admin.ModelAdmin):
    list_display = ("step_number", "title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("step_number", "title")

