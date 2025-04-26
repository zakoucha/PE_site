from django.apps import AppConfig


class LessonsConfig(AppConfig):
<<<<<<< HEAD
    default_auto_field = "django.db.models.BigAutoField"
    name = "lessons"

    def ready(self):
        from . import signals
=======
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lessons'
>>>>>>> 9c97bf9818e1437bed5150c0305042617a87cd4d
