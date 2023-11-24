from django.apps import AppConfig


class ModelmagicapiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ModelMagicAPI"

    def ready(self) -> None:
        from ModelMagicAPI.signals import discover_models
        discover_models(self)
