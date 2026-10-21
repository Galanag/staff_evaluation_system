from django.apps import AppConfig

class EvaluationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "evaluations"
    verbose_name = "Academic & Administrative Evaluation"

    def ready(self):
        from . import signals  # noqa: F401
