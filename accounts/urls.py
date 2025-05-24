# accounts/urls.py
from django.urls import path
from .views import ProfileUpdateView  # We’ll define this view

app_name = "accounts"  # Define the namespace

urlpatterns = [
    path("profile/update/", ProfileUpdateView.as_view(), name="profile_update"),
]
