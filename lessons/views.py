import logging
import os

from django.core.mail import send_mail
from django.views.decorators.cache import cache_page
from reportlab.pdfgen import canvas
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.views import View
from django.views.generic import TemplateView, DeleteView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
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
    CurriculumDocument,
    Student,
    Feedback,
)
from .forms import (
    LessonForm,
    ReviewForm,
    ReplyForm,
    LessonPlanForm,
    EquipmentForm,
    SafetyRuleForm,
    CurriculumDocumentForm,
    ContactForm,
)

logger = logging.getLogger(__name__)


class SharedLessonsView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "lessons/shared_lessons.html"
    context_object_name = "lessons"

    def get_queryset(self):
        return Lesson.objects.filter(shareable=True).exclude(author=self.request.user)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_lessons"] = Lesson.objects.filter(author=self.request.user)
        context["recent_lessons"] = Lesson.objects.all().order_by("-created_at")[:5]
        context["activities"] = Activity.objects.filter(grade_level__in=[1, 2, 3])[:6]
        context["form"] = ContactForm()
        return context


class ContactView(SuccessMessageMixin, FormView):
    form_class = ContactForm
    template_name = "lessons/contact.html"
    success_url = reverse_lazy("lessons:dashboard")
    success_message = "Thank you for your feedback! We'll get back to you soon."

    def form_valid(self, form):
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]
        email = form.cleaned_data["email"] or self.request.user.email

        # Save to database
        Feedback.objects.create(
            user=self.request.user, subject=subject, message=message, email=email
        )

        # Log feedback
        logger.info(
            f"Feedback received: Subject={subject}, Message={message}, Email={email}"
        )

        # Send email to admin
        try:
            send_mail(
                subject=f"New Feedback: {subject}",
                message=f"From: {self.request.user.username} ({email})\n\n{message}",
                from_email="no-reply@peportal.com",
                recipient_list=["zakidjebiri@outlook.com"],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Failed to send feedback email: {e}")

        return super().form_valid(form)


class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "lessons/lesson_form.html"
    success_url = reverse_lazy("lessons:lesson_list")

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
        return Lesson.objects.filter(author=self.request.user).order_by("-created_at")


class LessonDetailView(DetailView):
    model = Lesson
    template_name = "lessons/lesson_detail.html"
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm()
        context["reply_form"] = ReplyForm()
        return context

    def get_queryset(self):
        return Lesson.objects.select_related("author").prefetch_related("reviews")


class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = "equipment/equipment_list.html"
    context_object_name = "equipment"

    def get_queryset(self):
        # Check if user has a profile and school
        if (
            not hasattr(self.request.user, "profile")
            or not self.request.user.profile.school
        ):
            logger.warning(
                f"User {self.request.user.username} has no profile or school"
            )
            return Equipment.objects.none()
        queryset = Equipment.objects.filter(
            school=self.request.user.profile.school
        ).order_by("name")
        logger.debug(
            f"Queryset for user {self.request.user.username}: {queryset.count()} items"
        )
        return queryset


class EquipmentMixin(LoginRequiredMixin):
    model = Equipment
    form_class = EquipmentForm
    template_name = "equipment/form.html"
    success_url = reverse_lazy("lessons:equipment_list")

    def dispatch(self, request, *args, **kwargs):
        if not self._has_valid_school():
            messages.error(
                request,
                "Your account is not associated with a school. Please contact your administrator.",
            )
            logger.warning(
                f"User {request.user.username} blocked: No school association"
            )
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def _has_valid_school(self):
        return (
            hasattr(self.request.user, "profile")
            and self.request.user.profile.school is not None
        )

    def form_valid(self, form):
        # Set school and author for new equipment
        if not form.instance.pk:
            form.instance.school = self.request.user.profile.school
            form.instance.author = self.request.user
            logger.info(
                f"Creating equipment: {form.instance.name} for school {form.instance.school}"
            )
        else:
            logger.info(
                f"Updating equipment: {form.instance.name} (ID: {form.instance.pk})"
            )
        response = super().form_valid(form)
        # Add success message
        action = "updated" if form.instance.pk else "created"
        messages.success(
            self.request,
            f"Equipment '{form.instance.name}' has been {action} successfully.",
        )
        return response

    def form_invalid(self, form):
        # Log form errors for debugging
        logger.error(
            f"Form invalid for user {self.request.user.username}: {form.errors}"
        )
        messages.error(
            self.request,
            "There was an error saving the equipment. Please check the form.",
        )
        return super().form_invalid(form)


class EquipmentCreateView(EquipmentMixin, CreateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class EquipmentUpdateView(EquipmentMixin, UpdateView):
    def get_queryset(self):
        # Ensure users can only update their own equipment
        return Equipment.objects.filter(
            author=self.request.user, school=self.request.user.profile.school
        )


class EquipmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipment
    template_name = "equipment/equipment_confirm_delete.html"
    success_url = reverse_lazy("equipment_list")

    def dispatch(self, request, *args, **kwargs):
        equipment = self.get_object()
        if equipment.author != request.user:
            messages.error(request, "You can only delete equipment you created.")
            logger.warning(
                f"User {request.user.username} attempted to delete equipment ID {equipment.pk}"
            )
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        equipment = self.get_object()
        logger.info(
            f"Deleting equipment: {equipment.name} (ID: {equipment.pk}) by user {request.user.username}"
        )
        messages.success(
            request, f"Equipment '{equipment.name}' has been deleted successfully."
        )
        return super().delete(request, *args, **kwargs)


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


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/add_review.html"  # Use enhanced template

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.lesson = get_object_or_404(Lesson, pk=self.kwargs["pk"])
        logger.info(
            f"Creating review for lesson {form.instance.lesson.pk} by user {self.request.user.username}"
        )
        response = super().form_valid(form)
        messages.success(self.request, "Your review has been added successfully!")
        return response

    def form_invalid(self, form):
        logger.error(
            f"Form invalid for user {self.request.user.username}: {form.errors}"
        )
        messages.error(
            self.request,
            "There was an error submitting your review. Please check the form.",
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("lessons:lesson_detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lesson"] = get_object_or_404(Lesson, pk=self.kwargs["pk"])
        return context


class LikeReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, review_id):
        try:
            review = get_object_or_404(Review, id=review_id)
            if request.user in review.likes.all():
                review.likes.remove(request.user)
                liked = False
                action = "unliked"
            else:
                review.likes.add(request.user)
                liked = True
                action = "liked"
            logger.info(f"User {request.user.username} {action} review {review_id}")
            return Response(
                {
                    "likes": review.total_likes(),
                    "liked": liked,
                    "message": f"Review {action} successfully",
                }
            )
        except Exception as e:
            logger.error(f"Error in LikeReviewAPIView for review {review_id}: {str(e)}")
            return Response(
                {"error": "Failed to process like/unlike action"}, status=400
            )


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
            messages.success(request, "Reply added successfully!")
        else:
            messages.error(request, "Error adding reply. Please check the form.")
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


class LessonPlanGeneratorView(LoginRequiredMixin, FormView):
    form_class = LessonPlanForm
    template_name = "lessons/plan_generator.html"
    success_url = reverse_lazy("lessons:dashboard")

    def form_valid(self, form):
        lessons = Lesson.objects.filter(
            grade_level=form.cleaned_data["grade_level"],
            activity_type__in=form.cleaned_data["activity_types"],
        )
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="lesson_plan.pdf"'
        p = canvas.Canvas(response)
        y = 800
        for lesson in lessons:
            p.drawString(100, y, f"{lesson.title} (Grade {lesson.grade_level})")
            y -= 20
            if lesson.description:
                p.drawString(100, y, f"Description: {lesson.description[:100]}")
                y -= 20
        p.showPage()
        p.save()
        return response


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
            "lessons:grade_documents",
            kwargs={"grade": self.object.grade, "doc_type": self.object.document_type},
        )
