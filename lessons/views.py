import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
)
from .models import Lesson, Review
from .forms import LessonForm, ReviewForm, ReplyForm


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "lessons/lesson_form.html"
    success_url = reverse_lazy("lesson_list")

    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.author = self.request.user  # Set the author to the current user
        lesson.save()
        messages.success(self.request, "Lesson added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        messages.error(self.request, "Error adding lesson. Please check the form.")
        return super().form_invalid(form)


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "lessons/lesson_form.html"
    success_url = reverse_lazy("lesson_list")

    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.author = self.object.author  # Keep the existing author
        lesson.save()
        messages.success(self.request, "Lesson updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        messages.error(self.request, "Error updating lesson. Please check the form.")
        return super().form_invalid(form)


def lesson_download_file(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if lesson.file:
        file_path = lesson.file.path
        file_name = os.path.basename(file_path)

        # Force content type to application/octet-stream
        response = FileResponse(open(file_path, "rb"), as_attachment=True)
        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'

        return response

    return HttpResponse("No file available for download.", status=404)


class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    context_object_name = "lesson_list"
    template_name = "lessons/lesson_list.html"
    login_url = "account_login"


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    context_object_name = "lesson"
    template_name = "lessons/lesson_detail.html"
    login_url = "account_login"
    permission_required = "lessons.special_status"
    queryset = Lesson.objects.all().prefetch_related("reviews__author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm()
        context["reply_form"] = ReplyForm()
        return context


class SearchResultsListView(ListView):
    model = Lesson
    context_object_name = "lesson_list"
    template_name = "lessons/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Lesson.objects.filter(Q(title__icontains=query))


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "lessons/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lessons"] = Lesson.objects.filter(author=self.request.user)
        return context


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "lessons/add_review.html"

    def form_valid(self, form):
        review = form.save(commit=False)
        review.author = self.request.user
        review.lesson = get_object_or_404(Lesson, pk=self.kwargs["pk"])
        review.save()
        messages.success(self.request, "Review added successfully!")
        return redirect("lesson_detail", pk=self.kwargs["pk"])


class LikeReviewAPIView(LoginRequiredMixin, APIView):
    def post(self, request, review_id, *args, **kwargs):
        review = get_object_or_404(Review, id=review_id)
        if request.user in review.likes.all():
            review.likes.remove(request.user)  # Unlike
            liked = False
        else:
            review.likes.add(request.user)  # Like
            liked = True
        return Response(
            {"likes": review.total_likes(), "liked": liked}, status=status.HTTP_200_OK
        )


@login_required
def reply_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.lesson = (
                review.lesson
            )  # Ensure the reply is linked to the correct lesson
            reply.parent = review  # Correctly links reply to the parent review
            reply.save()
            print("Reply saved successfully!")
            messages.success(request, "Reply added successfully!")
        else:
            print("Form errors:", form.errors)
    return redirect("lesson_detail", pk=review.lesson.pk)
