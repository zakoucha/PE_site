from django.urls import path
from .views import (
    LessonListView,
    LessonDetailView,
    LessonCreateView,
    LessonUpdateView,
    lesson_download_file,
    SearchResultsListView,
    UserDashboardView,
    ReviewCreateView,
    LikeReviewAPIView,
    reply_review,
)


urlpatterns = [
    path("", LessonListView.as_view(), name="lesson_list"),
    path("<uuid:pk>", LessonDetailView.as_view(), name="lesson_detail"),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path("dashboard/", UserDashboardView.as_view(), name="dashboard"),
    path("add/", LessonCreateView.as_view(), name="add_lesson"),
    path("update/<uuid:pk>/", LessonUpdateView.as_view(), name="update_lesson"),
    path("download/<uuid:pk>", lesson_download_file, name="download_lesson"),
    path("lesson/<uuid:pk>/review/", ReviewCreateView.as_view(), name="add_review"),
    path(
        "api/reviews/like/<int:review_id>/",
        LikeReviewAPIView.as_view(),
        name="like_review_api",
    ),
    path("reviews/reply/<int:review_id>/", reply_review, name="reply_review"),
]
