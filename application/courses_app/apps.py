from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings
from django.db.models.signals import post_save

class Сourses_appConfig(AppConfig):
    name = 'courses_app'
    def ready(self):
        from .signals import populate_models
        post_migrate.connect(populate_models, sender=self)
        from .signals import create_user_profile
        post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)


