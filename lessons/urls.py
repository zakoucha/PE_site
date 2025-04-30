from django.urls import path
from .views import (
    LessonListView,
    LessonDetailView,
    LessonCreateView,
    LessonUpdateView,
    LessonDeleteView,
    lesson_download_file,
    SearchResultsListView,
    UserDashboardView,
    ReviewCreateView,
    LikeReviewAPIView,
    reply_review,
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
    DocumentListView,
    CurriculumDownloadView,
    DocumentVersionHistoryView,
    CreateNewVersionView,
    DocumentUploadView,
)

urlpatterns = [
    # Lesson-related URLs
    path("", LessonListView.as_view(), name="lesson_list"),
    path("<uuid:pk>/", LessonDetailView.as_view(), name="lesson_detail"),
    path("add/", LessonCreateView.as_view(), name="add_lesson"),
    path("update/<uuid:pk>/", LessonUpdateView.as_view(), name="update_lesson"),
    path("lessons/<uuid:pk>/delete/", LessonDeleteView.as_view(), name="delete_lesson"),
    path("download/<uuid:pk>/", lesson_download_file, name="download_lesson"),
    # Search and Dashboard
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path("dashboard/", UserDashboardView.as_view(), name="dashboard"),
    # Review system
    path("lesson/<uuid:pk>/review/", ReviewCreateView.as_view(), name="add_review"),
    path(
        "api/reviews/like/<int:review_id>/",
        LikeReviewAPIView.as_view(),
        name="like_review_api",
    ),
    path("reviews/reply/<int:review_id>/", reply_review, name="reply_review"),
    # PE-Specific Features
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
    # Safety and Profile
    path("safety/", SafetyGuidelinesView.as_view(), name="safety_guidelines"),
    path("safety/add/", SafetyRuleCreateView.as_view(), name="safety_rule_add"),
    path(
        "safety/<int:pk>/delete/",
        SafetyRuleDeleteView.as_view(),
        name="safety_rule_delete",
    ),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile_update"),
    path(
        "documents/<int:grade>/<str:doc_type>/",
        DocumentListView.as_view(),
        name="grade_documents",
    ),
    path(
        "download-curriculum/<int:pk>/",
        CurriculumDownloadView.as_view(),
        name="download_curriculum",
    ),
    path(
        "document/<int:pk>/versions/",
        DocumentVersionHistoryView.as_view(),
        name="document_version_history",
    ),
    path(
        "document/<int:pk>/new-version/",
        CreateNewVersionView.as_view(),
        name="create_new_version",
    ),
    path("documents/upload/", DocumentUploadView.as_view(), name="upload_document"),
]
