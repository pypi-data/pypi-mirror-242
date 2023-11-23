from django.apps import AppConfig


class InitiativesConfig(AppConfig):
    name = "modules.initiatives"
    verbose_name = "3. Инициативы"
    plug_in = True

    def ready(self) -> None:
        from .signals import get_instanse_before_save, \
        signaling_for_create_initiative, \
        signaling_for_delete_initiative

