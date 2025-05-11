from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from lessons.models import Lesson


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_lessons"] = Lesson.objects.filter(author=self.request.user)
        context["recent_lessons"] = Lesson.objects.all().order_by("-created_at")[:5]
        return context


class AboutPageView(TemplateView):
    template_name = "about.html"
