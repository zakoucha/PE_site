from django import forms
from .models import (
    Lesson,
    Review,
    Equipment,
    Activity,
    SkillAssessment,
    School,
    SafetyRule,
    CurriculumDocument,
)


class LessonForm(forms.ModelForm):
    ACTIVITY_TYPES = [
        ("warmup", "Warm-up Activity"),
        ("main", "Main Activity"),
        ("cool", "Cool-down Activity"),
        ("game", "Game"),
        ("skill", "Skill Development"),
    ]

    GRADE_LEVELS = [(i, f"Grade {i}") for i in range(1, 7)]

    activity_type = forms.ChoiceField(choices=ACTIVITY_TYPES)
    grade_level = forms.ChoiceField(choices=GRADE_LEVELS)
    objectives = forms.MultipleChoiceField(
        choices=[
            ("motor", "Motor Skills"),
            ("fitness", "Physical Fitness"),
            ("social", "Social Skills"),
            ("cognitive", "Cognitive Development"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Lesson
        fields = [
            "title",
            "description",
            "age_group",
            "grade_level",
            "activity_type",
            "duration",
            "objectives",
            "equipment_needed",
            "file",
            "cover",
        ]
        widgets = {
            "duration": forms.NumberInput(attrs={"min": 5, "max": 60}),
            "objectives": forms.TextInput(attrs={"data-role": "tagsinput"}),
            "age_group": forms.Select(choices=Lesson.AGE_GROUP_CHOICES),
            "equipment_needed": forms.CheckboxSelectMultiple,
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review"]
        widgets = {"review": forms.Textarea(attrs={"rows": 3})}


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review"]
        widgets = {"review": forms.Textarea(attrs={"rows": 2})}


# PE-SPECIFIC FORMS


class LessonPlanForm(forms.Form):
    GRADE_CHOICES = [(i, f"Grade {i}") for i in range(1, 6)]

    grade_level = forms.ChoiceField(choices=GRADE_CHOICES)
    duration = forms.IntegerField(
        min_value=15, max_value=60, help_text="Total lesson duration in minutes"
    )
    objectives = forms.MultipleChoiceField(
        choices=[
            ("motor", "Motor Skills"),
            ("fitness", "Physical Fitness"),
            ("social", "Social Skills"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    equipment_available = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["equipment_available"].queryset = Equipment.objects.filter(
                school=user.profile.school
            )


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ["name", "quantity", "storage_location", "condition"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not hasattr(self.user, "profile") or not self.user.profile.school:
            raise forms.ValidationError(
                "You must be associated with a school to add equipment"
            )
        return cleaned_data


class SkillAssessmentForm(forms.ModelForm):
    class Meta:
        model = SkillAssessment
        fields = ["skill", "score", "notes"]
        widgets = {
            "score": forms.Select(
                choices=[
                    (1, "Beginning"),
                    (2, "Developing"),
                    (3, "Proficient"),
                    (4, "Advanced"),
                ]
            ),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            "name",
            "description",
            "activity_type",
            "duration",
            "intensity_level",
            "grade_level",
            "objectives",
            "equipment_needed",
        ]


class SafetyRuleForm(forms.ModelForm):
    class Meta:
        model = SafetyRule
        fields = ["title", "description", "category", "reference"]


class CurriculumDocumentForm(forms.ModelForm):
    class Meta:
        model = CurriculumDocument
        fields = [
            "grade",
            "document_type",
            "trimester",
            "academic_year",
            "title",
            "file",
        ]
        widgets = {
            "academic_year": forms.TextInput(attrs={"placeholder": "2023-2024"}),
            "trimester": forms.Select(choices=CurriculumDocument.TRIMESTER_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["trimester"].required = False


class ContactForm(forms.Form):
    subject = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Subject"})
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Your feedback or suggestion", "rows": 5}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Your email (optional)"}),
        required=False,
    )
