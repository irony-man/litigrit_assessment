from django.apps import AppConfig


class LlmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "llm"

    def ready(self):
        import llm.signals  # noqa
