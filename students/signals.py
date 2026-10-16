import re
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student

User = get_user_model()


def clean_phone_for_username(phone):
    """Extract only digits from phone number for clean username."""
    if not phone:
        return ""
    digits = re.sub(r"\D", "", phone)
    return digits


@receiver(post_save, sender=Student)
def create_or_update_student_user(sender, instance, created, **kwargs):
    """
    Signal: Automatically creates a User account for every new Student.
    Synchronizes user details if the student's profile is updated.
    """
    # Parse first and last names
    parts = instance.full_name.strip().split(maxsplit=1)
    first_name = parts[0] if parts else ""
    last_name = parts[1] if len(parts) > 1 else ""

    phone_digits = clean_phone_for_username(instance.phone)

    if not instance.user:
        # Determine unique username
        candidate_username = phone_digits if phone_digits else f"student_{instance.id}"
        if User.objects.filter(username=candidate_username).exists():
            candidate_username = f"student_{instance.id}_{phone_digits[-4:]}" if len(phone_digits) >= 4 else f"student_{instance.id}"

        # Default password can be the phone number or 'student123'
        raw_password = phone_digits if len(phone_digits) >= 6 else "student123"

        user = User(
            username=candidate_username,
            first_name=first_name,
            last_name=last_name,
            email=instance.email or "",
            phone=instance.phone or "",
            role="student",
            is_staff=False,
            is_active=True,
        )
        user.set_password(raw_password)
        user.save()

        # Update without re-triggering recursive post_save
        Student.objects.filter(id=instance.id).update(user=user)
    else:
        # Synchronize details
        user = instance.user
        updated = False
        if user.first_name != first_name:
            user.first_name = first_name
            updated = True
        if user.last_name != last_name:
            user.last_name = last_name
            updated = True
        if instance.email and user.email != instance.email:
            user.email = instance.email
            updated = True
        if instance.phone and user.phone != instance.phone:
            user.phone = instance.phone
            updated = True
        if updated:
            user.save()
