from django.apps import AppConfig


class EcologyConfig(AppConfig):
    name = "modules.ecology"
    verbose_name = "7. Бонусная программа"
    plug_in = True

    def ready(self) -> None:
        from .signals import get_event_instanse_before_save, get_goods_n_service_item_instanse_before_save, \
            signaling_for_create_event, signaling_for_create_goods_n_service, signaling_for_delete_event, \
            signaling_for_delete_goods_n_service_item
        
