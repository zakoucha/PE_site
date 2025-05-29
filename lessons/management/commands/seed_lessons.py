from django.core.management.base import BaseCommand
from lessons.models import Lesson

from accounts.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Lesson.objects.create(
            title="Tag Game: Freeze Tag",
            author=CustomUser.objects.first(),
            grade_level=1,
            activity_type="game",
            description="Students run and freeze when tagged.",
            duration=20,
        )
