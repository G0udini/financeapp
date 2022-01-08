from django.apps import AppConfig


class StockConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stock"

    def ready(self):
        from .signals import create_user_profile, save_user_profile
