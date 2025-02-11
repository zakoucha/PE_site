from django.test import TestCase
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Lesson, Review

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

    def test_lesson_list_view_for_logged_in_user(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        response = self.client.get(reverse("lesson_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")
        self.assertTemplateUsed(response, "lessons/lesson_list.html")

    def test_lesson_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse("lesson_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "%s?next=/lessons/" % (reverse("account_login")))
        response = self.client.get("%s?next=/lessons/" % (reverse("account_login")))
        self.assertContains(response, "Log In")

    def test_lesson_detail_view(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        response = self.client.get(self.lesson.get_absolute_url())
        no_response = self.client.get("lessons/&éé/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "test")
        self.assertContains(response, "An excellent review")
        self.assertTemplateUsed(response, "lessons/lesson_detail.html")
