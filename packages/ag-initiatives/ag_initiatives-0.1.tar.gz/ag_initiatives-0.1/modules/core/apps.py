from django.apps import AppConfig



class CoreConfig(AppConfig):
    name = "modules.core"
    verbose_name = "1. Общее"
    plug_in = False

    def ready(self):
        import modules.core.signals.department_archiving
        import modules.core.signals.user_balance
        import modules.core.signals.active_citizen_module
