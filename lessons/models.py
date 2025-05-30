import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth import get_user_model

User = get_user_model()


class Lesson(models.Model):
    ACTIVITY_TYPES = [
        ("warmup", "Warm-up"),
        ("main", "Main Activity"),
        ("game", "Game"),
        ("skill", "Skill Development"),
        ("cool", "Cool-down"),
    ]
    AGE_GROUP_CHOICES = [
        ("child", "Child (6-12)"),
        ("teen", "Teen (13-19)"),
        ("adult", "Adult (20+)"),
    ]
    GRADE_LEVELS = [(i, f"Grade {i}") for i in range(1, 6)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lessons"
    )
    description = models.TextField()
    file = models.FileField(upload_to="lesson_files/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    shareable = models.BooleanField(
        default=False, help_text="Allow other teachers to view"
    )
    # PE-Specific Fields
    activity_type = models.CharField(
        max_length=20, choices=ACTIVITY_TYPES, default="main"
    )
    grade_level = models.IntegerField(choices=GRADE_LEVELS, default=1)
    duration = models.PositiveIntegerField(help_text="Duration in minutes", default=30)
    video_url = models.URLField(blank=True, null=True)
    age_group = models.CharField(
        max_length=20, choices=AGE_GROUP_CHOICES, null=True, blank=True
    )
    objectives = ArrayField(
        models.CharField(max_length=20),
        blank=True,
        default=list,
        help_text="Learning objectives",
    )
    equipment_needed = models.ManyToManyField(
        "Equipment", blank=True, related_name="lessons"
    )

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_index"),
            models.Index(fields=["grade_level"], name="grade_level_index"),
            models.Index(fields=["activity_type"], name="activity_type_index"),
        ]
        ordering = ["-created_at"]
        permissions = [
            ("special_status", "Can read all lessons"),
        ]

    def __str__(self):
        return f"{self.title} (Grade {self.grade_level})"

    def get_absolute_url(self):
        return reverse("lessons:lesson_detail", kwargs={"pk": self.pk})


class CurriculumDocument(models.Model):
    DOCUMENT_TYPES = [
        ("session_sheet", "Session Sheet"),
        ("annual_program", "Annual Program"),
        ("annual_distribution", "Annual Distribution"),
        ("trimester_clip", "Trimester Clip"),
        ("curriculum", "Physical Education Curriculum"),
    ]

    GRADE_CHOICES = [(i, f"Grade {i}") for i in range(1, 6)]
    TRIMESTER_CHOICES = [(1, "First"), (2, "Second"), (3, "Third")]
    version = models.PositiveIntegerField(default=1)
    previous_version = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_versions",
    )
    is_current = models.BooleanField(default=True)
    changelog = models.TextField(
        blank=True, help_text="Describe changes from previous version"
    )
    grade = models.IntegerField(choices=GRADE_CHOICES)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    trimester = models.IntegerField(choices=TRIMESTER_CHOICES, null=True, blank=True)
    academic_year = models.CharField(max_length=9)  # Format: 2023-2024
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="curriculum_documents/")
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_documents",
    )

    class Meta:
        ordering = ["grade", "document_type", "-version"]
        unique_together = [("grade", "document_type", "academic_year", "version")]

    def __str__(self):
        return f"{self.get_grade_display()} - {self.get_document_type_display()} ({self.academic_year})"


class Equipment(models.Model):
    CONDITION_CHOICES = [
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("fair", "Fair"),
        ("poor", "Poor"),
    ]

    name = models.CharField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="equipment",
        null=True,
    )
    quantity = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)
    storage_location = models.CharField(max_length=100)
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default="good"
    )
    school = models.ForeignKey(
        "School", on_delete=models.CASCADE, related_name="equipment"
    )

    def __str__(self):
        return f"{self.name} ({self.quantity})"


class School(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.name


class Activity(models.Model):
    INTENSITY_LEVELS = [("low", "Low"), ("moderate", "Moderate"), ("high", "High")]
    ACTIVITY_TYPES = [
        ("warmup", "Warm-up"),
        ("main", "Main Activity"),
        ("cool", "Cool-down"),
        ("game", "Game"),
        ("skill", "Skill Development"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    activity_type = models.CharField(
        max_length=20, choices=ACTIVITY_TYPES, default="main"
    )
    intensity_level = models.CharField(max_length=20, choices=INTENSITY_LEVELS)
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="activities",
        blank=True,
        null=True,
    )
    grade_level = models.IntegerField(choices=Lesson.GRADE_LEVELS, default=1)
    equipment_needed = models.ManyToManyField(Equipment, blank=True)
    objectives = ArrayField(models.CharField(max_length=20), blank=True, default=list)
    image = models.ImageField(upload_to="activity_images/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_intensity_level_display()})"


class SkillAssessment(models.Model):
    SKILL_CHOICES = [
        ("throw", "Throwing"),
        ("catch", "Catching"),
        ("run", "Running"),
        ("jump", "Jumping"),
        ("strike", "Striking"),
    ]

    RATING_CHOICES = [
        (1, "Beginning"),
        (2, "Developing"),
        (3, "Proficient"),
        (4, "Advanced"),
    ]

    student = models.ForeignKey(
        "Student", on_delete=models.CASCADE, related_name="skills_assessed"
    )
    skill = models.CharField(max_length=20, choices=SKILL_CHOICES)
    score = models.IntegerField(choices=RATING_CHOICES)
    notes = models.TextField(blank=True)
    assessed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ["student", "skill", "date"]

    def __str__(self):
        return f"{self.student} - {self.get_skill_display()} ({self.score})"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    grade_level = models.IntegerField(choices=Lesson.GRADE_LEVELS)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Grade {self.grade_level})"


class SafetyRule(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General Safety"),
        ("equipment", "Equipment Use"),
        ("emergency", "Emergency Procedures"),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    reference = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    review = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_reviews", blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f"{self.author} - {self.review[:20]}"

    def total_likes(self):
        return self.likes.count()


class Feedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="feedbacks",
    )
    subject = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} by {self.user or self.email}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
