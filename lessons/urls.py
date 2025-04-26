from django.urls import path
from .views import (
    LessonListView,
    LessonDetailView,
    LessonCreateView,
    LessonUpdateView,
<<<<<<< HEAD
    LessonDeleteView,
=======
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d
    lesson_download_file,
    SearchResultsListView,
    UserDashboardView,
    ReviewCreateView,
    LikeReviewAPIView,
    reply_review,
<<<<<<< HEAD
    LessonPlanGeneratorView,
    LessonPlanResultView,
    EquipmentListView,
    EquipmentCreateView,
    EquipmentUpdateView,
    ActivityBankView,
    ProgressTrackerView,
    SafetyGuidelinesView,
    ProfileUpdateView,
    SafetyRuleCreateView,
    SafetyRuleDeleteView,
    EquipmentDeleteView,
)

urlpatterns = [
    # Existing URLs
    path("", LessonListView.as_view(), name="lesson_list"),
    path("<uuid:pk>/", LessonDetailView.as_view(), name="lesson_detail"),
=======
)


urlpatterns = [
    path("", LessonListView.as_view(), name="lesson_list"),
    path("<uuid:pk>", LessonDetailView.as_view(), name="lesson_detail"),
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path("dashboard/", UserDashboardView.as_view(), name="dashboard"),
    path("add/", LessonCreateView.as_view(), name="add_lesson"),
    path("update/<uuid:pk>/", LessonUpdateView.as_view(), name="update_lesson"),
<<<<<<< HEAD
    path("lessons/<uuid:pk>/delete/", LessonDeleteView.as_view(), name="delete_lesson"),
=======
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d
    path("download/<uuid:pk>", lesson_download_file, name="download_lesson"),
    path("lesson/<uuid:pk>/review/", ReviewCreateView.as_view(), name="add_review"),
    path(
        "api/reviews/like/<int:review_id>/",
        LikeReviewAPIView.as_view(),
        name="like_review_api",
    ),
    path("reviews/reply/<int:review_id>/", reply_review, name="reply_review"),
<<<<<<< HEAD
    # New PE-Specific URLs
    path("plan-generator/", LessonPlanGeneratorView.as_view(), name="plan_generator"),
    path("plan-result/", LessonPlanResultView.as_view(), name="plan_result"),
    path("equipment/", EquipmentListView.as_view(), name="equipment_list"),
    path("equipment/add/", EquipmentCreateView.as_view(), name="equipment_add"),
    path(
        "equipment/<int:pk>/delete/",
        EquipmentDeleteView.as_view(),
        name="equipment_delete",
    ),
    path(
        "equipment/<int:pk>/edit/", EquipmentUpdateView.as_view(), name="equipment_edit"
    ),
    path("activities/<str:type>/", ActivityBankView.as_view(), name="activity_bank"),
    path("progress/", ProgressTrackerView.as_view(), name="progress_tracker"),
    path("safety/", SafetyGuidelinesView.as_view(), name="safety_guidelines"),
    path("safety/add/", SafetyRuleCreateView.as_view(), name="safety_rule_add"),
    path(
        "safety/<int:pk>/delete/",
        SafetyRuleDeleteView.as_view(),
        name="safety_rule_delete",
    ),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile_update"),
=======
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d
]
