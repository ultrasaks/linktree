from django.apps import AppConfig


class CustomingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customing_app'
