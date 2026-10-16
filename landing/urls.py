from django.urls import path
from . import views

app_name = "landing"

# ─── PUBLIC ENDPOINTS ────────────────────────────────────────────────────────
public_patterns = [
    # All-in-one landing page data
    path("landing/", views.LandingPageView.as_view(), name="landing-page"),

    # Site settings
    path("settings/", views.SiteSettingsView.as_view(), name="site-settings"),

    # Hero
    path("hero/", views.HeroSectionView.as_view(), name="hero"),
    path("hero-slides/", views.HeroSlideListView.as_view(), name="hero-slide-list"),

    # Statistics
    path("statistics/", views.StatisticListView.as_view(), name="statistics"),

    # Courses
    path("courses/", views.CourseListView.as_view(), name="course-list"),
    path("courses/<slug:slug>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("course-categories/", views.CourseCategoryListView.as_view(), name="course-category-list"),

    # Mentors
    path("mentors/", views.MentorListView.as_view(), name="mentor-list"),
    path("mentors/<int:pk>/", views.MentorDetailView.as_view(), name="mentor-detail"),

    # Student results / reels
    path("results/", views.StudentResultListView.as_view(), name="result-list"),

    # Learning process
    path("learning-process/", views.LearningProcessListView.as_view(), name="learning-process-list"),

    # Partners
    path("partners/", views.PartnerListView.as_view(), name="partner-list"),

    # Graduates
    path("graduates/", views.GraduateListView.as_view(), name="graduate-list"),

    # Testimonials
    path("testimonials/", views.TestimonialListView.as_view(), name="testimonial-list"),

    # FAQ
    path("faq/", views.FAQListView.as_view(), name="faq-list"),

    # Blog
    path("blog/", views.BlogPostListView.as_view(), name="blog-list"),
    path("blog/<slug:slug>/", views.BlogPostDetailView.as_view(), name="blog-detail"),
    path("blog/categories/", views.BlogCategoryListView.as_view(), name="blog-category-list"),

    # About
    path("about/", views.AboutSectionView.as_view(), name="about"),

    # Forms (write-only for public)
    path("apply/", views.ApplicationCreateView.as_view(), name="apply"),
    path("contact/", views.ContactMessageCreateView.as_view(), name="contact"),
]

# ─── ADMIN ENDPOINTS ─────────────────────────────────────────────────────────
admin_patterns = [
    # Settings
    path("admin/settings/", views.SiteSettingsUpdateView.as_view(), name="admin-settings"),

    # Hero
    path("admin/hero/", views.HeroSectionAdminListCreate.as_view(), name="admin-hero-list"),
    path("admin/hero/<int:pk>/", views.HeroSectionAdminDetail.as_view(), name="admin-hero-detail"),
    path("admin/hero-slides/", views.HeroSlideAdminListCreate.as_view(), name="admin-hero-slide-list"),
    path("admin/hero-slides/<int:pk>/", views.HeroSlideAdminDetail.as_view(), name="admin-hero-slide-detail"),

    # Statistics
    path("admin/statistics/", views.StatisticAdminListCreate.as_view(), name="admin-stat-list"),
    path("admin/statistics/<int:pk>/", views.StatisticAdminDetail.as_view(), name="admin-stat-detail"),

    # Course categories
    path("admin/course-categories/", views.CourseCategoryAdminListCreate.as_view(), name="admin-cat-list"),
    path("admin/course-categories/<int:pk>/", views.CourseCategoryAdminDetail.as_view(), name="admin-cat-detail"),

    # Courses
    path("admin/courses/", views.CourseAdminListCreate.as_view(), name="admin-course-list"),
    path("admin/courses/<int:pk>/", views.CourseAdminDetail.as_view(), name="admin-course-detail"),
    path("admin/courses/<int:course_pk>/features/", views.CourseFeatureAdminListCreate.as_view(), name="admin-feature-list"),
    path("admin/courses/<int:course_pk>/features/<int:pk>/", views.CourseFeatureAdminDetail.as_view(), name="admin-feature-detail"),

    # Mentors
    path("admin/mentors/", views.MentorAdminListCreate.as_view(), name="admin-mentor-list"),
    path("admin/mentors/<int:pk>/", views.MentorAdminDetail.as_view(), name="admin-mentor-detail"),

    # Student results / reels
    path("admin/results/", views.StudentResultAdminListCreate.as_view(), name="admin-result-list"),
    path("admin/results/<int:pk>/", views.StudentResultAdminDetail.as_view(), name="admin-result-detail"),

    # Learning process
    path("admin/learning-process/", views.LearningProcessAdminListCreate.as_view(), name="admin-process-list"),
    path("admin/learning-process/<int:pk>/", views.LearningProcessAdminDetail.as_view(), name="admin-process-detail"),

    # Partners
    path("admin/partners/", views.PartnerAdminListCreate.as_view(), name="admin-partner-list"),
    path("admin/partners/<int:pk>/", views.PartnerAdminDetail.as_view(), name="admin-partner-detail"),

    # Graduates
    path("admin/graduates/", views.GraduateAdminListCreate.as_view(), name="admin-graduate-list"),
    path("admin/graduates/<int:pk>/", views.GraduateAdminDetail.as_view(), name="admin-graduate-detail"),

    # Testimonials
    path("admin/testimonials/", views.TestimonialAdminListCreate.as_view(), name="admin-testimonial-list"),
    path("admin/testimonials/<int:pk>/", views.TestimonialAdminDetail.as_view(), name="admin-testimonial-detail"),

    # FAQ
    path("admin/faq/", views.FAQAdminListCreate.as_view(), name="admin-faq-list"),
    path("admin/faq/<int:pk>/", views.FAQAdminDetail.as_view(), name="admin-faq-detail"),

    # Blog categories
    path("admin/blog/categories/", views.BlogCategoryAdminListCreate.as_view(), name="admin-blog-cat-list"),
    path("admin/blog/categories/<int:pk>/", views.BlogCategoryAdminDetail.as_view(), name="admin-blog-cat-detail"),

    # Blog posts
    path("admin/blog/", views.BlogPostAdminListCreate.as_view(), name="admin-blog-list"),
    path("admin/blog/<int:pk>/", views.BlogPostAdminDetail.as_view(), name="admin-blog-detail"),

    # Applications
    path("admin/applications/", views.ApplicationAdminListView.as_view(), name="admin-app-list"),
    path("admin/applications/<int:pk>/", views.ApplicationAdminDetail.as_view(), name="admin-app-detail"),
    path("admin/applications/<int:pk>/convert-to-student/", views.ApplicationConvertToStudentView.as_view(), name="admin-app-convert"),

    # Contact messages
    path("admin/contacts/", views.ContactMessageAdminListView.as_view(), name="admin-contact-list"),
    path("admin/contacts/<int:pk>/", views.ContactMessageAdminDetail.as_view(), name="admin-contact-detail"),

    # About section
    path("admin/about/", views.AboutSectionAdminListCreate.as_view(), name="admin-about-list"),
    path("admin/about/<int:pk>/", views.AboutSectionAdminDetail.as_view(), name="admin-about-detail"),
]

urlpatterns = public_patterns + admin_patterns
