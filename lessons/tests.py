from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Lesson

User = get_user_model()


class LessonTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="admin", password="password123")

        cls.lesson = Lesson.objects.create(
            title="test",
            description="text",
            author=cls.user,
        )

    def test_lesson_listing(self):
        self.assertEqual(f"{self.lesson.title}", "test")
        self.assertEqual(f"{self.lesson.description}", "text")
        self.assertEqual(f"{self.lesson.author}", "admin")

    def test_lesson_list_view(self):
        response = self.client.get(reverse("lesson_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")
        self.assertTemplateUsed(response, "lessons/lesson_list.html")

    def test_lesson_detail_view(self):
        response = self.client.get(self.lesson.get_absolute_url())
        no_response = self.client.get("lessons/&éé/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "test")
        self.assertTemplateUsed(response, "lessons/lesson_detail.html")
