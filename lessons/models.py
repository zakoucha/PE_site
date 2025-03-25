import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1,
    )
    description = models.TextField()
    file = models.FileField(upload_to="lesson_files/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_index"),
        ]

        permissions = [
            ("special_status", "Can read all books"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("lesson_detail", kwargs={"pk": self.pk})


class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    intensity_level = models.CharField(
        max_length=20,
        choices=[("Low", "Low"), ("Moderate", "Moderate"), ("High", "High")],
    )
    lesson = models.ForeignKey(
        "Lesson", on_delete=models.CASCADE, related_name="activities"
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    review = (
        models.TextField()
    )  # Changed from CharField to TextField for longer reviews
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_reviews", blank=True
    )

    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f"{self.author} - {self.review[:20]}"

    def total_likes(self):
        return self.likes.count()
