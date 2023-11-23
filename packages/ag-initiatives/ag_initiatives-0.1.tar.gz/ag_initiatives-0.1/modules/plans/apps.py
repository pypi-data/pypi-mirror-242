from django.apps import AppConfig


class PlansConfig(AppConfig):
    name = "modules.plans"
    verbose_name = "6. Планы"
    plug_in = True

    def ready(self):
        from .signals import plan_comment_signal
