from django.contrib import admin
<<<<<<< HEAD
from .models import Lesson, Activity, Review, Profile, SafetyRule

from django.contrib import admin
from django.utils.html import format_html
from .models import SafetyRule


@admin.register(SafetyRule)
class SafetyRuleAdmin(admin.ModelAdmin):
    list_display = ("title", "category_badge", "author", "reference_link", "created_at")
    list_filter = ("category", "author", "created_at")
    search_fields = ("title", "description")
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at", "reference_preview")

    fieldsets = (
        ("Rule Information", {"fields": ("title", "description", "category")}),
        (
            "References",
            {"fields": ("reference", "reference_preview"), "classes": ("collapse",)},
        ),
        (
            "Metadata",
            {
                "fields": ("author", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def category_badge(self, obj):
        colors = {
            "general": "bg-primary",
            "equipment": "bg-warning text-dark",
            "emergency": "bg-danger",
        }
        return format_html(
            '<span class="badge {}">{}</span>',
            colors.get(obj.category, "bg-secondary"),
            obj.get_category_display(),
        )

    category_badge.short_description = "Category"
    category_badge.admin_order_field = "category"

    def reference_link(self, obj):
        if obj.reference:
            return format_html(
                '<a href="{}" target="_blank">🔗 Reference</a>', obj.reference
            )
        return "-"

    reference_link.short_description = "Reference"

    def reference_preview(self, obj):
        if obj.reference:
            return format_html(
                '<iframe src="{}" width="100%" height="200px"></iframe>', obj.reference
            )
        return "-"

    reference_preview.short_description = "Preview"

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set author if creating new
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "school")
    search_fields = ("user__email", "school__name")
=======
from .models import Lesson, Activity, Review
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d


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
