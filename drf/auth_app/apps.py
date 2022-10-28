import time
from datetime import timedelta
from django.apps import AppConfig
from django.utils import timezone

from config.config import settings as config


class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'

    def ready(self):
        pass
        # ClearThread().start()