from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _



class TimeStampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqt"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan vaqt"))

    class Meta:
        abstract = True


# ─────────────────────────────────────────────
# 1. SITE SETTINGS
# ─────────────────────────────────────────────
class SiteSettings(TimeStampedModel):
    """Global site configuration – only ONE record should exist (singleton)."""
    site_name = models.CharField(max_length=100, default="ITeach", verbose_name=_("Sayt nomi"))
    logo = models.ImageField(upload_to="site/", null=True, blank=True, verbose_name=_("Logo"))
    favicon = models.ImageField(upload_to="site/", null=True, blank=True, verbose_name=_("Favicon"))
    phone = models.CharField(max_length=20, verbose_name=_("Telefon raqam"))
    phone_secondary = models.CharField(max_length=20, blank=True, verbose_name=_("Qo'shimcha telefon"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    address = models.CharField(max_length=255, blank=True, verbose_name=_("Manzil"))
    working_hours = models.CharField(max_length=100, blank=True, verbose_name=_("Ish vaqti"))
    telegram = models.URLField(blank=True, verbose_name=_("Telegram"))
    instagram = models.URLField(blank=True, verbose_name=_("Instagram"))
    youtube = models.URLField(blank=True, verbose_name=_("YouTube"))
    facebook = models.URLField(blank=True, verbose_name=_("Facebook"))
    tiktok = models.URLField(blank=True, verbose_name=_("TikTok"))
    linkedin = models.URLField(blank=True, verbose_name=_("LinkedIn"))
    map_embed_url = models.TextField(blank=True, verbose_name=_("Xarita embed URL"))
    meta_title = models.CharField(max_length=200, blank=True, verbose_name=_("SEO sarlavha"))
    meta_description = models.TextField(blank=True, verbose_name=_("SEO tavsif"))

    class Meta:
        verbose_name = _("Sayt sozlamasi")
        verbose_name_plural = _("Sayt sozlamalari")

    def __str__(self):
        return self.site_name


# ─────────────────────────────────────────────
# 2. HERO SECTION
# ─────────────────────────────────────────────
class HeroSection(TimeStampedModel):
    """Landing page hero / banner section."""
    badge_text = models.CharField(max_length=100, blank=True, verbose_name=_("Badge matni"))
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"))
    subtitle = models.TextField(verbose_name=_("Tavsif"))
    primary_btn_text = models.CharField(max_length=80, default="Kursga yozilish", verbose_name=_("Asosiy tugma matni"))
    primary_btn_link = models.CharField(max_length=200, default="#application", verbose_name=_("Asosiy tugma havolasi"))
    secondary_btn_text = models.CharField(max_length=80, blank=True, verbose_name=_("Ikkinchi tugma matni"))
    secondary_btn_link = models.CharField(max_length=200, blank=True, verbose_name=_("Ikkinchi tugma havolasi"))
    background_image = models.ImageField(upload_to="hero/", null=True, blank=True, verbose_name=_("Fon rasmi"))
    hero_image = models.ImageField(upload_to="hero/", null=True, blank=True, verbose_name=_("Hero rasmi"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))

    class Meta:
        verbose_name = _("Hero bo'lim")
        verbose_name_plural = _("Hero bo'limlar")

    def __str__(self):
        return self.title


class HeroSlide(TimeStampedModel):
    """Dynamic slides displayed on the right-side carousel of the Hero section."""
    hero_section = models.ForeignKey(
        HeroSection,
        on_delete=models.CASCADE,
        related_name="slides",
        null=True,
        blank=True,
        verbose_name=_("Hero bo'lim"),
    )
    title = models.CharField(max_length=200, verbose_name=_("Sarlavha (masalan: Dasturlash yo'nalishi)"))
    subtitle = models.CharField(max_length=255, verbose_name=_("Kichik sarlavha (masalan: Frontend, Backend va Mobile)"))
    icon = models.CharField(max_length=100, blank=True, verbose_name=_("Ikonka"))
    image = models.ImageField(upload_to="hero/slides/", null=True, blank=True, verbose_name=_("Slayd rasmi"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))

    class Meta:
        verbose_name = _("Hero slayd")
        verbose_name_plural = _("Hero slaydlar")
        ordering = ["order"]

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────
# 3. STATISTICS
# ─────────────────────────────────────────────
class Statistic(TimeStampedModel):
    """Key numbers shown in the stats section."""
    icon = models.CharField(max_length=100, blank=True, verbose_name=_("Ikonka (CSS class yoki emoji)"))
    value = models.CharField(max_length=50, verbose_name=_("Qiymat (masalan: 1000+)"))
    label = models.CharField(max_length=100, verbose_name=_("Tavsif (masalan: O'quvchilar)"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))

    class Meta:
        verbose_name = _("Statistika")
        verbose_name_plural = _("Statistikalar")
        ordering = ["order"]

    def __str__(self):
        return f"{self.value} - {self.label}"


# ─────────────────────────────────────────────
# 4. COURSES
# ─────────────────────────────────────────────
class CourseCategory(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name=_("Kategoriya nomi"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))

    class Meta:
        verbose_name = _("Kurs kategoriyasi")
        verbose_name_plural = _("Kurs kategoriyalari")
        ordering = ["order"]

    def __str__(self):
        return self.name


class Course(TimeStampedModel):
    LEVEL_CHOICES = [
        ("beginner", _("Boshlang'ich")),
        ("intermediate", _("O'rta")),
        ("advanced", _("Yuqori")),
    ]
    STATUS_CHOICES = [
        ("Faol", _("Faol")),
        ("Yaqinda", _("Yaqinda boshlanadi")),
        ("Yopiq", _("Qabul yopiq")),
    ]
    FORMAT_CHOICES = [
        ("online", _("Online kurs")),
        ("offline", _("Offline kurs")),
        ("hybrid", _("Gibrid kurs")),
    ]

    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name=_("Kategoriya"),
    )
    mentor = models.ForeignKey(
        "Mentor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_courses",
        verbose_name=_("Asosiy mentor"),
    )
    name = models.CharField(max_length=200, verbose_name=_("Kurs nomi"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    short_description = models.CharField(max_length=300, verbose_name=_("Qisqa tavsif"))
    description = models.TextField(blank=True, verbose_name=_("To'liq tavsif"))
    image = models.ImageField(upload_to="courses/", null=True, blank=True, verbose_name=_("Rasm"))
    icon = models.CharField(max_length=100, blank=True, verbose_name=_("Ikonka"))
    duration_months = models.PositiveSmallIntegerField(verbose_name=_("Davomiyligi (oy)"))
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="beginner", verbose_name=_("Daraja"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Faol", verbose_name=_("Holat"))
    course_format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default="online", verbose_name=_("Kurs formati"))
    students_count = models.PositiveIntegerField(default=0, verbose_name=_("O'quvchilar soni"))
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Narxi (so'm)"))
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Eski narx"))
    is_popular = models.BooleanField(default=False, verbose_name=_("Mashhurmi"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))

    class Meta:
        verbose_name = _("Kurs")
        verbose_name_plural = _("Kurslar")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class CourseFeature(models.Model):
    """Individual features/benefits listed under each course."""
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="features", verbose_name=_("Kurs")
    )
    text = models.CharField(max_length=200, verbose_name=_("Xususiyat matni"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))

    class Meta:
        verbose_name = _("Kurs xususiyati")
        verbose_name_plural = _("Kurs xususiyatlari")
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.name}: {self.text}"


# ─────────────────────────────────────────────
# 5. MENTORS
# ─────────────────────────────────────────────
class Mentor(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mentor_profile",
        verbose_name=_("Foydalanuvchi hisobi"),
    )
    name = models.CharField(max_length=150, verbose_name=_("Ism Familiya"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Telefon"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    position = models.CharField(max_length=150, verbose_name=_("Lavozim / yo'nalish"))
    bio = models.TextField(blank=True, verbose_name=_("Qisqa biografiya"))
    photo = models.ImageField(upload_to="mentors/", null=True, blank=True, verbose_name=_("Rasm"))
    experience_years = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tajriba (yil)"))
    courses = models.ManyToManyField(Course, blank=True, related_name="mentors", verbose_name=_("Kurslar"))
    telegram = models.URLField(blank=True, verbose_name=_("Telegram"))
    linkedin = models.URLField(blank=True, verbose_name=_("LinkedIn"))
    instagram = models.URLField(blank=True, verbose_name=_("Instagram"))
    github = models.URLField(blank=True, verbose_name=_("GitHub"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))

    class Meta:
        verbose_name = _("Mentor")
        verbose_name_plural = _("Mentorlar")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────
# 6. PARTNERS / COMPANIES
# ─────────────────────────────────────────────
class Partner(TimeStampedModel):
    name = models.CharField(max_length=150, verbose_name=_("Kompaniya nomi"))
    logo = models.ImageField(upload_to="partners/", null=True, blank=True, verbose_name=_("Logo"))
    website = models.URLField(blank=True, verbose_name=_("Veb-sayt"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))

    class Meta:
        verbose_name = _("Hamkor")
        verbose_name_plural = _("Hamkorlar")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────
# 7. GRADUATES / SUCCESS STORIES
# ─────────────────────────────────────────────
class Graduate(TimeStampedModel):
    name = models.CharField(max_length=150, verbose_name=_("Ism Familiya"))
    photo = models.ImageField(upload_to="graduates/", null=True, blank=True, verbose_name=_("Rasm"))
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="graduates",
        verbose_name=_("Kurs"),
    )
    company = models.CharField(max_length=150, blank=True, verbose_name=_("Ishlayotgan kompaniya"))
    position = models.CharField(max_length=150, blank=True, verbose_name=_("Lavozim"))
    salary = models.CharField(max_length=50, blank=True, verbose_name=_("Maosh (ko'rsatish uchun)"))
    testimonial = models.TextField(blank=True, verbose_name=_("Sharhlar / fikrlar"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))

    class Meta:
        verbose_name = _("Bitiruvchi")
        verbose_name_plural = _("Bitiruvchilar")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────
# 8. FAQ
# ─────────────────────────────────────────────
class FAQ(TimeStampedModel):
    question = models.CharField(max_length=300, verbose_name=_("Savol"))
    answer = models.TextField(verbose_name=_("Javob"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))

    class Meta:
        verbose_name = _("Ko'p so'raladigan savol")
        verbose_name_plural = _("Ko'p so'raladigan savollar")
        ordering = ["order"]

    def __str__(self):
        return self.question


# ─────────────────────────────────────────────
# 9. BLOG
# ─────────────────────────────────────────────
class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name=_("Kategoriya nomi"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))

    class Meta:
        verbose_name = _("Blog kategoriyasi")
        verbose_name_plural = _("Blog kategoriyalari")

    def __str__(self):
        return self.name


class BlogPost(TimeStampedModel):
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name=_("Kategoriya"),
    )
    title = models.CharField(max_length=300, verbose_name=_("Sarlavha"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    excerpt = models.CharField(max_length=400, blank=True, verbose_name=_("Qisqa matn"))
    content = models.TextField(verbose_name=_("Maqola matni"))
    cover_image = models.ImageField(upload_to="blog/", null=True, blank=True, verbose_name=_("Muqova rasmi"))
    author = models.ForeignKey(
        Mentor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name=_("Muallif"),
    )
    is_published = models.BooleanField(default=False, verbose_name=_("Nashr etilganmi"))
    published_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Nashr sanasi"))
    views_count = models.PositiveIntegerField(default=0, verbose_name=_("Ko'rishlar soni"))

    class Meta:
        verbose_name = _("Blog maqolasi")
        verbose_name_plural = _("Blog maqolalari")
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────
# 10. APPLICATION (Lead form)
# ─────────────────────────────────────────────
class Application(TimeStampedModel):
    STATUS_CHOICES = [
        ("new", _("Yangi")),
        ("called", _("Qo'ng'iroq qilindi")),
        ("enrolled", _("Yozildi")),
        ("rejected", _("Rad etildi")),
    ]

    full_name = models.CharField(max_length=150, verbose_name=_("Ism Familiya"))
    phone = models.CharField(max_length=20, verbose_name=_("Telefon raqam"))
    direction = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("Qiziqayotgan yo'nalish"),
        help_text=_("Masalan: Dasturlash, SMM & Marketing, Sun'iy Intellekt, 3D Max"),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications",
        verbose_name=_("Kurs"),
    )
    message = models.TextField(blank=True, verbose_name=_("Xabar"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name=_("Holat"))
    notes = models.TextField(blank=True, verbose_name=_("Admin izohlari"))

    class Meta:
        verbose_name = _("Ariza")
        verbose_name_plural = _("Arizalar")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.phone}"


# ─────────────────────────────────────────────
# 11. CONTACT MESSAGE
# ─────────────────────────────────────────────
class ContactMessage(TimeStampedModel):
    full_name = models.CharField(max_length=150, verbose_name=_("Ism Familiya"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Telefon"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    subject = models.CharField(max_length=200, blank=True, verbose_name=_("Mavzu"))
    message = models.TextField(verbose_name=_("Xabar"))
    is_read = models.BooleanField(default=False, verbose_name=_("O'qilganmi"))

    class Meta:
        verbose_name = _("Xabar")
        verbose_name_plural = _("Xabarlar")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name}: {self.subject}"


# ─────────────────────────────────────────────
# 12. ABOUT SECTION
# ─────────────────────────────────────────────
class AboutSection(TimeStampedModel):
    title = models.CharField(max_length=200, verbose_name=_("Sarlavha"))
    subtitle = models.CharField(max_length=300, blank=True, verbose_name=_("Kichik sarlavha"))
    description = models.TextField(verbose_name=_("Tavsif"))
    image = models.ImageField(upload_to="about/", null=True, blank=True, verbose_name=_("Rasm"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))

    class Meta:
        verbose_name = _("Biz haqimizda bo'lim")
        verbose_name_plural = _("Biz haqimizda bo'limlari")

    def __str__(self):
        return self.title


class AboutFeature(models.Model):
    """Bullet points / advantages listed in About section."""
    about = models.ForeignKey(
        AboutSection, on_delete=models.CASCADE, related_name="features", verbose_name=_("Bo'lim")
    )
    icon = models.CharField(max_length=100, blank=True, verbose_name=_("Ikonka"))
    title = models.CharField(max_length=150, verbose_name=_("Sarlavha"))
    description = models.CharField(max_length=300, blank=True, verbose_name=_("Tavsif"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))

    class Meta:
        verbose_name = _("Ustunlik")
        verbose_name_plural = _("Ustunliklar")
        ordering = ["order"]

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────
# 13. TESTIMONIALS
# ─────────────────────────────────────────────
class Testimonial(TimeStampedModel):
    name = models.CharField(max_length=150, verbose_name=_("Ism"))
    photo = models.ImageField(upload_to="testimonials/", null=True, blank=True, verbose_name=_("Rasm"))
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials",
        verbose_name=_("Kurs"),
    )
    rating = models.PositiveSmallIntegerField(default=5, verbose_name=_("Baho (1-5)"))
    text = models.TextField(verbose_name=_("Sharh matni"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))

    class Meta:
        verbose_name = _("Sharh")
        verbose_name_plural = _("Sharhlar")
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} - {self.rating} yulduz"


# ─────────────────────────────────────────────
# 14. STUDENT RESULTS (Video Reels & Success)
# ─────────────────────────────────────────────
class StudentResult(TimeStampedModel):
    """Student result / video reel as seen on landing carousel and admin results."""
    name = models.CharField(max_length=150, verbose_name=_("O'quvchi / Markaz nomi (masalan: Najot Ta'lim)"))
    tag = models.CharField(max_length=100, blank=True, verbose_name=_("Teg / Natija (masalan: Dasturchi, Bitiruvchi)"))
    video_url = models.CharField(max_length=500, blank=True, verbose_name=_("Video URL (masalan: /imgs/Eldor.mp4 yoki CDN)"))
    video_file = models.FileField(upload_to="results/videos/", null=True, blank=True, verbose_name=_("Video fayl"))
    thumbnail = models.ImageField(upload_to="results/thumbs/", null=True, blank=True, verbose_name=_("Muqova rasmi"))
    instagram_url = models.URLField(blank=True, verbose_name=_("Instagram URL"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))

    class Meta:
        verbose_name = _("O'quvchi natijasi")
        verbose_name_plural = _("O'quvchilar natijalari")
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.name} ({self.tag})"


# ─────────────────────────────────────────────
# 15. LEARNING PROCESS (Ta'lim qanday amalga oshiriladi?)
# ─────────────────────────────────────────────
class LearningProcess(TimeStampedModel):
    """Workflow steps in the education process."""
    step_number = models.CharField(max_length=10, default="01", verbose_name=_("Bosqich raqami (masalan: 01)"))
    title = models.CharField(max_length=150, verbose_name=_("Sarlavha"))
    description = models.TextField(verbose_name=_("Tavsif"))
    icon = models.CharField(max_length=100, blank=True, verbose_name=_("Ikonka"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tartib"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))

    class Meta:
        verbose_name = _("Ta'lim bosqichi")
        verbose_name_plural = _("Ta'lim bosqichlari")
        ordering = ["order", "step_number"]

    def __str__(self):
        return f"{self.step_number} - {self.title}"



