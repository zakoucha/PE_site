import os
<<<<<<< HEAD

from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.views.generic import TemplateView, DeleteView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
<<<<<<< HEAD
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views import View
from .models import SkillAssessment
=======
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
<<<<<<< HEAD
    FormView,
    DeleteView,
)
from .models import (
    Lesson,
    Review,
    Equipment,
    Activity,
    SkillAssessment,
    SafetyRule,
    Profile,
)
from .forms import (
    LessonForm,
    ReviewForm,
    ReplyForm,
    LessonPlanForm,
    EquipmentForm,
    SkillAssessmentForm,
    ProfileForm,
    SafetyRuleForm,
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
=======
)
from .models import Lesson, Review
from .forms import LessonForm, ReviewForm, ReplyForm
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "lessons/lesson_form.html"
    success_url = reverse_lazy("lesson_list")

    def form_valid(self, form):
<<<<<<< HEAD
        # First save the lesson instance without M2M
        lesson = form.save(commit=False)
        lesson.author = self.request.user
        lesson.save()  # Must save before adding M2M relationships

        # Now save the many-to-many relationships
        form.save_m2m()  # This handles the equipment_needed relationship

        messages.success(self.request, "Lesson added successfully!")
        return super().form_valid(form)


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "lessons/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get recent lessons created by the user
        recent_lessons = Lesson.objects.filter(author=user).order_by("-created_at")[:5]

        # Get recent activities from the user's lessons
        recent_activities = Activity.objects.filter(lesson__author=user).order_by(
            "-lesson__created_at"
        )[:3]

        # Equipment count with proper profile/school checking
        equipment_count = 0
        if hasattr(user, "profile") and user.profile.school:
            equipment_count = Equipment.objects.filter(
                school=user.profile.school
            ).count()

        context.update(
            {
                "recent_lessons": recent_lessons,
                "recent_activities": recent_activities,
                "equipment_count": equipment_count,
            }
        )
        return context


class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = "lessons/lesson_delete.html"
    success_url = reverse_lazy("lesson_list")
=======
        lesson = form.save(commit=False)
        lesson.author = self.request.user  # Set the author to the current user
        lesson.save()
        messages.success(self.request, "Lesson added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        messages.error(self.request, "Error adding lesson. Please check the form.")
        return super().form_invalid(form)
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "lessons/lesson_form.html"
    success_url = reverse_lazy("lesson_list")

    def form_valid(self, form):
<<<<<<< HEAD
        messages.success(self.request, "Lesson updated successfully!")
        return super().form_valid(form)

=======
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

>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d

class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    context_object_name = "lesson_list"
    template_name = "lessons/lesson_list.html"
<<<<<<< HEAD
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if "q" in self.request.GET:
            return queryset.filter(
                Q(title__icontains=self.request.GET["q"])
                | Q(description__icontains=self.request.GET["q"])
            )
        return queryset.annotate(like_count=Count("reviews__likes"))
=======
    login_url = "account_login"
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
<<<<<<< HEAD
    template_name = "lessons/lesson_detail.html"
=======
    context_object_name = "lesson"
    template_name = "lessons/lesson_detail.html"
    login_url = "account_login"
    permission_required = "lessons.special_status"
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d
    queryset = Lesson.objects.all().prefetch_related("reviews__author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm()
        context["reply_form"] = ReplyForm()
<<<<<<< HEAD
        context["related_activities"] = Activity.objects.filter(
            grade_level=self.object.grade_level
        )[:3]
        return context


# PE-SPECIFIC VIEWS


class LessonPlanGeneratorView(LoginRequiredMixin, FormView):
    template_name = "lessons/plan_generator.html"
    form_class = LessonPlanForm
    success_url = reverse_lazy("plan_result")

    def form_valid(self, form):
        grade = form.cleaned_data["grade_level"]
        duration = form.cleaned_data["duration"]
        objectives = form.cleaned_data["objectives"]
        equipment = form.cleaned_data["equipment_available"]

        # Warmup with fallback
        warmup = self.get_warmup(grade)

        # Main activities with multiple fallback layers
        main_activities = self.get_main_activities(
            grade, duration, objectives, equipment
        )

        # Store in session
        self.request.session["generated_plan"] = {
            "warmup": warmup.id if warmup else None,
            "main_activities": list(main_activities.values_list("id", flat=True)),
            "generated_at": str(timezone.now()),
        }
        return super().form_valid(form)

    def get_warmup(self, grade):
        """Get warmup with multiple fallback strategies"""
        return (
            Activity.objects.filter(
                activity_type="warmup",
                grade_level=grade,
                duration__lte=10,  # Warmups shouldn't be too long
            )
            .order_by("?")
            .first()
            or Activity.objects.filter(activity_type="warmup").order_by("?").first()
        )

    def get_main_activities(self, grade, duration, objectives, equipment):
        """Get main activities with progressive fallbacks"""
        base_qs = Activity.objects.filter(
            activity_type="main",
            grade_level=grade,
            duration__lte=duration * 0.7,  # Use 70% of total duration
        )

        # Filter by available equipment
        if equipment:
            base_qs = base_qs.filter(equipment_needed__in=equipment).distinct()

        # First try: Match selected objectives
        if objectives:
            activities = base_qs.filter(objectives__overlap=objectives)[:3]
            if activities.exists():
                return activities

        # Fallback 1: Any objectives
        activities = base_qs.order_by("?")[:3]
        if activities.exists():
            return activities

        # Fallback 2: Any grade level
        return Activity.objects.filter(
            activity_type="main", duration__lte=duration
        ).order_by("?")[:3]


# lessons/views.py
class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = "equipment/equipment_list.html"
    context_object_name = "equipment"  # Add this line

    def get_queryset(self):
        if not hasattr(self.request.user, "profile"):
            return Equipment.objects.none()
        return Equipment.objects.filter(
            school=self.request.user.profile.school
        ).order_by("name")


class EquipmentCreateUpdateMixin(LoginRequiredMixin):
    model = Equipment
    form_class = EquipmentForm
    template_name = "equipment/form.html"
    success_url = reverse_lazy("equipment_list")

    def dispatch(self, request, *args, **kwargs):
        """Prevent access if user lacks school association"""
        if not self._has_valid_school():
            messages.error(
                request, "You must be associated with a school to manage equipment"
            )
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def _has_valid_school(self):
        """Check user profile and school association"""
        return (
            hasattr(self.request.user, "profile")
            and self.request.user.profile.school is not None
        )

    def form_valid(self, form):
        """Handle successful form submission"""
        # Set school for new equipment
        if not form.instance.pk:
            form.instance.school = self.request.user.profile.school
            form.instance.author = self.request.user

        action = "created" if not form.instance.pk else "updated"
        messages.success(
            self.request, f"Equipment '{form.instance.name}' {action} successfully!"
        )
        return super().form_valid(form)


class EquipmentCreateView(EquipmentCreateUpdateMixin, CreateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class EquipmentUpdateView(EquipmentCreateUpdateMixin, UpdateView):
    pass


class EquipmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipment
    template_name = "equipment/equipment_confirm_delete.html"
    success_url = reverse_lazy("equipment_list")

    def dispatch(self, request, *args, **kwargs):
        equipment = self.get_object()
        if equipment.author != request.user:
            messages.error(request, "You can only delete equipment you created")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class ActivityBankView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = "activities/bank.html"
    paginate_by = 10

    def get_queryset(self):
        default_grade = 1
        return Activity.objects.filter(
            activity_type=self.kwargs.get("type", "warmup"), grade_level=default_grade
        )


class ProgressTrackerView(LoginRequiredMixin, TemplateView):
    template_name = "progress/tracker.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get assessments for current user's students
        if hasattr(self.request.user, "profile") and self.request.user.profile.school:
            context["assessments"] = SkillAssessment.objects.filter(
                student__school=self.request.user.profile.school
            ).order_by("-date")
        else:
            context["assessments"] = SkillAssessment.objects.none()

        return context


class SafetyGuidelinesView(ListView):
    model = SafetyRule
    template_name = "safety/guidelines.html"  # This should match your template path
    context_object_name = "safety_rules"

    def get_queryset(self):
        return SafetyRule.objects.all().order_by("category")


class SafetyRuleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SafetyRule
    form_class = SafetyRuleForm
    template_name = "safety/safetyrule_form.html"
    success_message = "Safety rule was created successfully!"
    success_url = reverse_lazy("safety_guidelines")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add New Safety Rule"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user  # Auto-set the current user as author
        return super().form_valid(form)


class SafetyRuleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SafetyRule
    success_url = reverse_lazy("safety_guidelines")
    success_message = "Safety rule was deleted successfully!"
    template_name = "safety/safetyrule_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        # Only allow authors to delete their own rules
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied("You can only delete your own safety rules.")
        return super().dispatch(request, *args, **kwargs)


def lesson_download_file(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if lesson.file:
        return FileResponse(
            open(lesson.file.path, "rb"),
            as_attachment=True,
            filename=os.path.basename(lesson.file.path),
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


=======
        return context


>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d
class SearchResultsListView(ListView):
    model = Lesson
    context_object_name = "lesson_list"
    template_name = "lessons/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
<<<<<<< HEAD
        return Lesson.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(activities__name__icontains=query)
        ).distinct()


class LessonPlanResultView(LoginRequiredMixin, TemplateView):
    template_name = "lessons/plan_result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan_data = self.request.session.get("generated_plan", {})

        # Get activities from database using stored IDs
        context.update(
            {
                "warmup": Activity.objects.filter(id=plan_data.get("warmup")).first(),
                "main_activities": Activity.objects.filter(
                    id__in=plan_data.get("main_activities", [])
                ),
                "generated_at": plan_data.get("generated_at"),
            }
        )
        return context


=======
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


>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d
@login_required
def reply_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
<<<<<<< HEAD
            reply.lesson = review.lesson
            reply.parent = review
            reply.save()
            messages.success(request, "Reply added!")
=======
            reply.lesson = (
                review.lesson
            )  # Ensure the reply is linked to the correct lesson
            reply.parent = review  # Correctly links reply to the parent review
            reply.save()
            print("Reply saved successfully!")
            messages.success(request, "Reply added successfully!")
        else:
            print("Form errors:", form.errors)
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d
    return redirect("lesson_detail", pk=review.lesson.pk)
