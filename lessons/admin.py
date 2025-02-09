from django.contrib import admin
from .models import Lesson, Activity, Review


class ActivityInline(admin.TabularInline):
    model = Activity  # Corrected model


class ReviewInline(admin.TabularInline):  # Added inheritance from admin.TabularInline
    model = Review


class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "description",
    )
    inlines = [ReviewInline, ActivityInline]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "lesson",
        "duration",
        "intensity_level",
    )
    list_filter = ("intensity_level", "lesson")
    search_fields = ("name", "description")
    ordering = ("name",)
    list_per_page = 20

    fieldsets = (
        ("Basic Information", {"fields": ("name", "description")}),
        ("Activity Details", {"fields": ("duration", "intensity_level", "lesson")}),
    )


admin.site.register(Lesson, LessonAdmin)
