from django import forms
from .models import Lesson, Review


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "description", "file", "cover"]  # Fields relevant to Lesson


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review"]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review"]
