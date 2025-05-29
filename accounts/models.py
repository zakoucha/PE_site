from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    school = models.ForeignKey(
        "School", on_delete=models.SET_NULL, null=True, blank=True
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class School(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()
