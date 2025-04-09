from django.test import TestCase
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Lesson, Review
from PIL import Image
import io

User = get_user_model()


class LessonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="reviewuser",
            email="reviewuser@email.com",
            password="testpass123",
        )
        # Add necessary permissions
        special_permission = Permission.objects.get(codename="special_status")
        cls.user.user_permissions.add(special_permission)

        cls.lesson = Lesson.objects.create(
            title="test",
            description="text",
            author=cls.user,
        )
        cls.review = Review.objects.create(
            lesson=cls.lesson,
            author=cls.user,
            review="An excellent review",
        )

    def create_test_image_file(self):
        # Create a simple image file
        image = Image.new("RGB", (100, 100), color=(73, 109, 137))
        byte_arr = io.BytesIO()
        image.save(byte_arr, format="JPEG")
        byte_arr.seek(0)
        return SimpleUploadedFile(
            "test.jpg", byte_arr.read(), content_type="image/jpeg"
        )

    def test_create_lesson(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        response = self.client.post(
            reverse("add_lesson"),
            data={
                "title": "New Lesson",
                "description": "A test lesson",
                "file": SimpleUploadedFile(
                    "testfile.txt", b"Lesson file content"
                ),  # Example file field
                "cover": self.create_test_image_file(),  # Valid image file
            },
        )
        if response.status_code == 200:  # Form failed, print errors
            print("Form Errors:", response.context["form"].errors)

        self.assertEqual(response.status_code, 302)  # Expect redirect

    def test_update_lesson(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        response = self.client.post(
            reverse("update_lesson", args=[self.lesson.pk]),
            data={
                "title": "Updated Lesson Title",
                "description": "Updated description.",
                "file": SimpleUploadedFile(
                    "updatedfile.txt", b"Updated file content"
                ),  # Example file field
                "cover": self.create_test_image_file(),  # Valid image file
            },
        )
        if response.status_code == 200:  # Form failed, print errors
            print("Form Errors:", response.context["form"].errors)

        self.assertEqual(response.status_code, 302)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson Title")

    # Other tests...


class LikeReviewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.lesson = Lesson.objects.create(
            title="Sample Lesson",
            description="Lesson description",
            author=self.user,  # Ensure lesson has a valid author
        )
        self.review = Review.objects.create(
            author=self.user, lesson=self.lesson, review="Great lesson!"
        )

    def test_like_review(self):
        """Test that a user can like a review."""
        self.review.likes.add(self.user)
        self.assertEqual(self.review.likes.count(), 1)

    def test_prevent_duplicate_likes(self):
        """Test that a user cannot like the same review multiple times."""
        self.review.likes.add(self.user)
        self.review.likes.add(self.user)  # Attempt to like again
        self.assertEqual(self.review.likes.count(), 1)


class ReplyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.lesson = Lesson.objects.create(
            title="Sample Lesson",
            description="Lesson description",
            author=self.user,  # Ensure lesson has a valid author
        )
        self.parent_review = Review.objects.create(
            author=self.user, lesson=self.lesson, review="Great lesson!"
        )

    def test_add_reply_to_review(self):
        """Test that a reply can be added to a review."""
        reply = Review.objects.create(
            author=self.user,
            lesson=self.lesson,
            review="Thanks for your feedback!",
            parent=self.parent_review,  # Linking it as a reply
        )
        self.assertEqual(self.parent_review.replies.count(), 1)
        self.assertEqual(
            self.parent_review.replies.first().review, "Thanks for your feedback!"
        )
