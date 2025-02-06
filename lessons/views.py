from django.views.generic import ListView, DetailView
from .models import Lesson


class LessonListView(ListView):
    model = Lesson
    context_object_name = "lesson_list"
    template_name = "lessons/lesson_list.html"


class LessonDetailView(DetailView):
    model = Lesson
    context_object_name = "lesson"
    template_name = "lessons/lesson_detail.html"
