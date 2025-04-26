from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile


@receiver(post_save, sender=get_user_model())
def handle_user_profile(sender, instance, created, **kwargs):

    if created:
        # Use get_or_create to prevent duplicates
        Profile.objects.get_or_create(user=instance)
    else:
        # Only try to save if profile exists
        if hasattr(instance, "profile"):
            instance.profile.save()
