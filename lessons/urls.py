from django.urls import path
from .views import LessonListView, LessonDetailView, SearchResultsListView

urlpatterns = [
    path("", LessonListView.as_view(), name="lesson_list"),
    path("<uuid:pk>", LessonDetailView.as_view(), name="lesson_detail"),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
]
