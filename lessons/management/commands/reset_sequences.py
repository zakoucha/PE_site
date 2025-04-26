from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Reset database sequences"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Corrected SQL query
            cursor.execute(
                """
                SELECT setval(
                    pg_get_serial_sequence('lessons_profile', 'user_id'), 
                    COALESCE(MAX(user_id), 1), 
                    MAX(user_id) IS NOT NULL
                ) FROM lessons_profile;
            """
            )
            self.stdout.write(self.style.SUCCESS("Successfully reset sequences"))
