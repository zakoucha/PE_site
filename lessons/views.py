import os
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, DeleteView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from .models import (
    Lesson,
    Review,
    Equipment,
    Activity,
    SkillAssessment,
    SafetyRule,
    Profile,
    CurriculumDocument,
)
from .forms import (
    LessonForm,
    ReviewForm,
    ReplyForm,
    LessonPlanForm,
    EquipmentForm,
    ProfileForm,
    SafetyRuleForm,
    CurriculumDocumentForm,
)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profile_update.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"] = {"school": self.object.school}
        return kwargs


class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "lessons/lesson_form.html"
    success_url = reverse_lazy("lesson_list")

    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.author = self.request.user
        lesson.save()
        form.save_m2m()  # Save many-to-many relationships
        messages.success(self.request, "Lesson added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error adding lesson. Please check the form.")
        return super().form_invalid(form)


class LessonDeleteView(DeleteView):
    model = Lesson
    success_url = reverse_lazy("lesson_list")
    template_name = "lessons/lesson_delete.html"


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "lessons/lesson_form.html"
    success_url = reverse_lazy("lesson_list")

    def form_valid(self, form):
        messages.success(self.request, "Lesson updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating lesson. Please check the form.")
        return super().form_invalid(form)


class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    context_object_name = "lesson_list"
    template_name = "lessons/lesson_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if search_query := self.request.GET.get("q"):
            return queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
            )
        return queryset.annotate(like_count=Count("reviews__likes"))


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lessons/lesson_detail.html"
    queryset = Lesson.objects.all().prefetch_related("reviews__author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "review_form": ReviewForm(),
                "reply_form": ReplyForm(),
                "related_activities": Activity.objects.filter(
                    grade_level=self.object.grade_level
                )[:3],
            }
        )
        return context


class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = "equipment/equipment_list.html"
    context_object_name = "equipment"

    def get_queryset(self):
        if not hasattr(self.request.user, "profile"):
            return Equipment.objects.none()
        return Equipment.objects.filter(
            school=self.request.user.profile.school
        ).order_by("name")


class EquipmentMixin(LoginRequiredMixin):
    model = Equipment
    form_class = EquipmentForm
    template_name = "equipment/form.html"
    success_url = reverse_lazy("equipment_list")

    def dispatch(self, request, *args, **kwargs):
        if not self._has_valid_school():
            messages.error(request, "School association required")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def _has_valid_school(self):
        return (
            hasattr(self.request.user, "profile") and self.request.user.profile.school
        )

    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.school = self.request.user.profile.school
            form.instance.author = self.request.user
        return super().form_valid(form)


class EquipmentCreateView(EquipmentMixin, CreateView):
    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "user": self.request.user}


class EquipmentUpdateView(EquipmentMixin, UpdateView):
    pass


class EquipmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipment
    template_name = "equipment/equipment_confirm_delete.html"
    success_url = reverse_lazy("equipment_list")

    def dispatch(self, request, *args, **kwargs):
        equipment = self.get_object()
        if equipment.author != request.user:
            messages.error(request, "Can only delete your own equipment")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class SafetyRuleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SafetyRule
    form_class = SafetyRuleForm
    template_name = "safety/safetyrule_form.html"
    success_url = reverse_lazy("safety_guidelines")
    success_message = "Safety rule created successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SafetyRuleDeleteView(LoginRequiredMixin, DeleteView):
    model = SafetyRule
    success_url = reverse_lazy("safety_guidelines")
    template_name = "safety/safetyrule_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied("Can only delete your own rules")
        return super().dispatch(request, *args, **kwargs)


def lesson_download_file(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if lesson.file:
        return FileResponse(
            open(lesson.file.path, "rb"),
            filename=os.path.basename(lesson.file.path),
            as_attachment=True,
        )
    return HttpResponse("No file available", status=404)


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.lesson = get_object_or_404(Lesson, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("lesson_detail", kwargs={"pk": self.kwargs["pk"]})


class LikeReviewAPIView(APIView):
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.user in review.likes.all():
            review.likes.remove(request.user)
            liked = False
        else:
            review.likes.add(request.user)
            liked = True
        return Response({"likes": review.total_likes(), "liked": liked})


@login_required
def reply_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.lesson = review.lesson
            reply.parent = review
            reply.save()
            messages.success(request, "Reply added!")
    return redirect("lesson_detail", pk=review.lesson.pk)


class SearchResultsListView(ListView):
    model = Lesson
    template_name = "lessons/search_results.html"
    context_object_name = "lesson_list"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Lesson.objects.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(activity_type__icontains=query)
            )
        return Lesson.objects.none()


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "lessons/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get lessons created by the current user
        context["user_lessons"] = Lesson.objects.filter(author=self.request.user)
        # Add any other dashboard data you need
        return context


class LessonPlanGeneratorView(FormView):
    template_name = "lessons/plan_generator.html"
    form_class = LessonPlanForm
    success_url = reverse_lazy("lesson_list")  # Or your preferred success URL

    def form_valid(self, form):
        # Process the form data and generate lesson plan
        # You can customize this based on your requirements
        grade_level = form.cleaned_data["grade_level"]
        duration = form.cleaned_data["duration"]
        objectives = form.cleaned_data["objectives"]
        equipment = form.cleaned_data["equipment_available"]

        # Add your lesson plan generation logic here
        # For example, you might create a new Lesson object:
        lesson = Lesson.objects.create(
            title=f"Generated Lesson Plan for Grade {grade_level}",
            author=self.request.user,
            grade_level=grade_level,
            duration=duration,
            # ... other fields ...
        )
        lesson.equipment_needed.set(equipment)

        return super().form_valid(form)


class LessonPlanResultView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lessons/plan_result.html"
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data you need for the result view
        return context


class ActivityBankView(ListView):
    model = Activity
    template_name = "activities/bank.html"
    context_object_name = "activities"
    paginate_by = 10  # Show 10 activities per page

    def get_queryset(self):
        queryset = super().get_queryset()
        activity_type = self.kwargs.get("type")

        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)

        # Add search functionality
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        return queryset.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activity_type"] = self.kwargs.get("type", "all")
        context["search_query"] = self.request.GET.get("q", "")
        return context


class ProgressTrackerView(LoginRequiredMixin, ListView):
    template_name = "progress/tracker.html"
    context_object_name = "students"

    def get_queryset(self):
        # Get students for the current teacher's school
        return Student.objects.filter(
            school=self.request.user.profile.school
        ).prefetch_related("skills_assessed")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add skill choices to context
        context["skill_choices"] = SkillAssessment.SKILL_CHOICES

        # Add progress data for each student
        students_progress = []
        for student in context["students"]:
            student_data = {"student": student, "skills": {}}

            for skill_code, skill_name in SkillAssessment.SKILL_CHOICES:
                assessments = student.skills_assessed.filter(skill=skill_code)
                if assessments.exists():
                    latest = assessments.latest("date")
                    student_data["skills"][skill_code] = {
                        "latest_score": latest.score,
                        "latest_date": latest.date,
                        "progress": self._calculate_progress(assessments),
                    }

            students_progress.append(student_data)

        context["students_progress"] = students_progress
        return context

    def _calculate_progress(self, assessments):
        """Calculate progress trend based on multiple assessments"""
        if assessments.count() < 2:
            return "No trend data"

        first = assessments.earliest("date").score
        last = assessments.latest("date").score

        if last > first:
            return "Improving"
        elif last < first:
            return "Declining"
        return "Stable"


class SafetyGuidelinesView(ListView):
    model = SafetyRule
    template_name = "safety/guidelines.html"
    context_object_name = "safety_rules"
    paginate_by = 10  # Show 10 rules per page

    def get_queryset(self):
        queryset = super().get_queryset()

        # Add filtering by category if specified
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)

        return queryset.order_by("category", "title")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = SafetyRule.CATEGORY_CHOICES
        context["current_category"] = self.request.GET.get("category")
        return context


class DocumentListView(LoginRequiredMixin, ListView):
    model = CurriculumDocument
    template_name = "documents/document_list.html"
    context_object_name = "documents"

    def get_queryset(self):
        return CurriculumDocument.objects.filter(
            grade=self.kwargs.get("grade"), document_type=self.kwargs.get("doc_type")
        ).order_by("-academic_year")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "selected_grade": self.kwargs.get("grade"),
                "selected_type": self.kwargs.get("doc_type"),
            }
        )
        return context


class CurriculumDownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        document = get_object_or_404(CurriculumDocument, pk=kwargs["pk"])
        return FileResponse(open(document.file.path, "rb"), as_attachment=True)


class DocumentVersionHistoryView(LoginRequiredMixin, ListView):
    template_name = "documents/version_history.html"
    context_object_name = "versions"

    def get_queryset(self):
        base_doc = get_object_or_404(CurriculumDocument, pk=self.kwargs["pk"])
        return CurriculumDocument.objects.filter(
            grade=base_doc.grade,
            document_type=base_doc.document_type,
            academic_year=base_doc.academic_year,
        ).order_by("-version")


class CreateNewVersionView(LoginRequiredMixin, CreateView):
    model = CurriculumDocument
    fields = ["file", "changelog"]
    template_name = "documents/new_version.html"

    def get_initial(self):
        original = get_object_or_404(CurriculumDocument, pk=self.kwargs["pk"])
        return {
            "grade": original.grade,
            "document_type": original.document_type,
            "academic_year": original.academic_year,
            "title": original.title,
        }

    def form_valid(self, form):
        original = get_object_or_404(CurriculumDocument, pk=self.kwargs["pk"])

        # Set all previous versions as not current
        CurriculumDocument.objects.filter(
            grade=original.grade,
            document_type=original.document_type,
            academic_year=original.academic_year,
        ).update(is_current=False)

        form.instance.version = original.version + 1
        form.instance.previous_version = original
        form.instance.is_current = True
        form.instance.grade = original.grade
        form.instance.document_type = original.document_type
        form.instance.academic_year = original.academic_year
        form.instance.title = original.title

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("document_version_history", kwargs={"pk": self.object.pk})


class DocumentUploadView(LoginRequiredMixin, CreateView):
    model = CurriculumDocument
    form_class = CurriculumDocumentForm
    template_name = "documents/upload_document.html"

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "grade_documents",
            kwargs={"grade": self.object.grade, "doc_type": self.object.document_type},
        )
