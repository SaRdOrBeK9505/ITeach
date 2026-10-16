import re
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mentor

User = get_user_model()


def clean_phone_for_username(phone):
    if not phone:
        return ""
    return re.sub(r"\D", "", phone)


@receiver(post_save, sender=Mentor)
def create_or_update_mentor_user(sender, instance, created, **kwargs):
    """
    Signal: Automatically creates a User account for every new Mentor.
    Grants role='mentor', is_staff=True so mentors can access teacher portals.
    """
    parts = instance.name.strip().split(maxsplit=1)
    first_name = parts[0] if parts else ""
    last_name = parts[1] if len(parts) > 1 else ""

    phone_digits = clean_phone_for_username(instance.phone)

    if not instance.user:
        # Determine candidate username
        candidate_username = phone_digits if phone_digits else f"mentor_{instance.id}"
        if User.objects.filter(username=candidate_username).exists():
            candidate_username = f"mentor_{instance.id}_{phone_digits[-4:]}" if len(phone_digits) >= 4 else f"mentor_{instance.id}"

        raw_password = phone_digits if len(phone_digits) >= 6 else "mentor123"

        user = User(
            username=candidate_username,
            first_name=first_name,
            last_name=last_name,
            email=instance.email or "",
            phone=instance.phone or "",
            role="mentor",
            is_staff=True,
            is_active=True,
        )
        user.set_password(raw_password)
        user.save()

        # Update without re-triggering post_save
        Mentor.objects.filter(id=instance.id).update(user=user)
    else:
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
