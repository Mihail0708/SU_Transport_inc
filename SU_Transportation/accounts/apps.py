from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "SU_Transportation.accounts"

    def ready(self):
        result = super().ready()
        from . import signals
        return result

