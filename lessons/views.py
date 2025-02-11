from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Lesson


class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    context_object_name = "lesson_list"
    template_name = "lessons/lesson_list.html"
    login_url = "account_login"


class LessonDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Lesson
    context_object_name = "lesson"
    template_name = "lessons/lesson_detail.html"
    login_url = "account_login"
    permission_required = "lessons.special_status"
