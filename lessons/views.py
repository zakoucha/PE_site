from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
)
from .models import Lesson
from .forms import LessonForm


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "lessons/lesson_form.html"
    success_url = reverse_lazy("lesson_list")

    def form_valid(self, form):
        lesson = form.save(commit=False)  # Save but don't commit yet
        lesson.save()  # Now commit the save
        messages.success(self.request, "Lesson added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Debugging: Print errors to console
        messages.error(self.request, "Error adding lesson. Please check the form.")
        return super().form_invalid(form)


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "lessons/lesson_form.html"
    success_url = reverse_lazy("lesson_list")

    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.save()
        messages.success(self.request, "Lesson updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        messages.error(self.request, "Error updating lesson. Please check the form.")
        return super().form_invalid(form)


def lesson_download_file(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if lesson.uploaded_file:
        return FileResponse(open(lesson.uploaded_file.path, "rb"), as_attachment=True)
    else:
        return HttpResponse("No file available for download.", status=404)


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
    queryset = Lesson.objects.all().prefetch_related(
        "reviews__author",
    )


class SearchResultsListView(ListView):
    model = Lesson
    context_object_name = "lesson_list"
    template_name = "lessons/search_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Lesson.objects.filter(Q(title__icontains=query))


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "lessons/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lessons"] = Lesson.objects.filter(author=self.request.user)
        return context
