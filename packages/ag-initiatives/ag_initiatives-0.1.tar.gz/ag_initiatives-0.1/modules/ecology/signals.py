from des.models import DynamicEmailConfiguration
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from modules.ecology.models.event import Event
from modules.ecology.models.goods_n_services_item import GoodsNServicesItem
from modules.integration.enums.signals_event_type import SignalsEventType
from modules.integration.services.signals_serializer import SignalSerializer
from modules.integration.task import send_signal_for_api


@receiver(pre_save, sender=GoodsNServicesItem)
def get_goods_n_service_item_instanse_before_save(
    sender, instance: GoodsNServicesItem, **kwargs
):
    if instance.pk:
        setattr(
            instance, "_previous_state_instance", sender.objects.get(pk=instance.pk)
        )


@receiver(post_save, sender=GoodsNServicesItem)
def signaling_for_create_goods_n_service(
    sender, instance: GoodsNServicesItem, **kwargs
):
    if previous_instance := getattr(instance, "_previous_state_instance", None):
        # If goods_n_service_item was unpublished - send signal with message about this.
        if instance.is_published and (not previous_instance.is_published):
            # send_signal_for_api.delay(
            #     data=SignalSerializer(
            #         {
            #             "data_type": "REWARDS",
            #             "event_type": SignalsEventType.PUBLISH,
            #             "event_resource": instance.pk,
            #         }
            #     ).data
            # )
        # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Публикация поощрения"
            message = f"""
                    "data_type": "REWARDS",
                    "event_type": {SignalsEventType.PUBLISH}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=False)

        # If goods_n_service_item was published - send signal with message about publishing.
        elif (not instance.is_published) and previous_instance.is_published:
            # send_signal_for_api.delay(
            #     data=SignalSerializer(
            #         {
            #             "data_type": "REWARDS",
            #             "event_type": SignalsEventType.UNPUBLISH,
            #             "event_resource": instance.pk,
            #         }
            #     ).data
            # )
            # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Снятие с публикации поощрения"
            message = f"""
                    "data_type": "REWARDS",
                    "event_type": {SignalsEventType.UNPUBLISH}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=False)

        # Send message, that goods_n_service_item was changed.
        else:
            # send_signal_for_api.delay(
            #     data=SignalSerializer(
            #         {
            #             "data_type": "REWARDS",
            #             "event_type": SignalsEventType.UPDATE,
            #             "event_resource": instance.pk,
            #         }
            #     ).data
            # )
            # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Изменение поощрения"
            message = f"""
                    "data_type": "REWARDS",
                    "event_type": {SignalsEventType.UPDATE}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=False)

    else:
        # send_signal_for_api.delay(
        #     data=SignalSerializer(
        #         {
        #             "data_type": "REWARDS",
        #             "event_type": SignalsEventType.CREATE,
        #             "event_resource": instance.pk,
        #         }
        #     ).data
        # )
        # FIX @korchizhinskijna: Delete this notification by email
        from_email = str(DynamicEmailConfiguration.get_solo().from_email)
        to_email = ["drodikova@yandex.ru"]
        subject = "Создание поощрения"
        message = f"""
                "data_type": "REWARDS",
                "event_type": {SignalsEventType.CREATE}
                "event_resource": {instance.pk}
        """
        send_mail(subject, message, from_email, to_email, fail_silently=False)


@receiver(post_delete, sender=GoodsNServicesItem)
def signaling_for_delete_goods_n_service_item(
    sender, instance: GoodsNServicesItem, **kwargs
):
    # send_signal_for_api.delay(
    #     data=SignalSerializer(
    #         {
    #             "data_type": "REWARDS",
    #             "event_type": SignalsEventType.DELETE,
    #             "event_resource": instance.pk,
    #         }
    #     ).data
    # )
    # FIX @korchizhinskijna: Delete this notification by email
    from_email = str(DynamicEmailConfiguration.get_solo().from_email)
    to_email = ["drodikova@yandex.ru"]
    subject = "Удаление поощрения"
    message = f"""
            "data_type": "REWARDS",
            "event_type": {SignalsEventType.DELETE}
            "event_resource": {instance.pk}
    """
    send_mail(subject, message, from_email, to_email, fail_silently=False)


@receiver(pre_save, sender=Event)
def get_event_instanse_before_save(sender, instance: GoodsNServicesItem, **kwargs):
    if instance.pk:
        setattr(
            instance, "_previous_state_instance", sender.objects.get(pk=instance.pk)
        )


@receiver(post_save, sender=Event)
def signaling_for_create_event(sender, instance: Event, **kwargs):
    if previous_instance := getattr(instance, "_previous_state_instance", None):
        # If event was unpublished - send signal with message about this.
        if instance.is_published and (not previous_instance.is_published):
            # send_signal_for_api.delay(
            #     data=SignalSerializer(
            #         {
            #             "data_type": "OFFERS",
            #             "event_type": SignalsEventType.PUBLISH,
            #             "event_resource": instance.pk,
            #         }
            #     ).data
            # )
        # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Публикация предложения"
            message = f"""
                    "data_type": "OFFERS",
                    "event_type": {SignalsEventType.PUBLISH}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=False)

        # If event was published - send signal with message about publishing.
        elif (not instance.is_published) and previous_instance.is_published:
            # send_signal_for_api.delay(
            #     data=SignalSerializer(
            #         {
            #             "data_type": "OFFERS",
            #             "event_type": SignalsEventType.UNPUBLISH,
            #             "event_resource": instance.pk,
            #         }
            #     ).data
            # )
        # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Снятие с публикации предложения"
            message = f"""
                    "data_type": "OFFERS",
                    "event_type": {SignalsEventType.UNPUBLISH}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=False)

        # Send message, that event was changed.
        else:
            # send_signal_for_api.delay(
            #     data=SignalSerializer(
            #         {
            #             "data_type": "OFFERS",
            #             "event_type": SignalsEventType.UPDATE,
            #             "event_resource": instance.pk,
            #         }
            #     ).data
            # )
        # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Изменение предложения"
            message = f"""
                    "data_type": "OFFERS",
                    "event_type": {SignalsEventType.UPDATE}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=False)

    else:
        # send_signal_for_api.delay(data=SignalSerializer({
        #     "data_type": "OFFERS",
        #     "event_type": SignalsEventType.CREATE,
        #     "event_resource": instance.pk,
        # }).data)
    # FIX @korchizhinskijna: Delete this notification by email
        from_email = str(DynamicEmailConfiguration.get_solo().from_email)
        to_email = ["drodikova@yandex.ru"]
        subject = "Создание предложения"
        message = f"""
                "data_type": "OFFERS",
                "event_type": {SignalsEventType.CREATE}
                "event_resource": {instance.pk}
        """
        send_mail(subject, message, from_email, to_email, fail_silently=False)


@receiver(post_delete, sender=Event)
def signaling_for_delete_event(sender, instance: Event, **kwargs):
    # send_signal_for_api.delay(
    #     data=SignalSerializer(
    #         {
    #             "data_type": "OFFERS",
    #             "event_type": SignalsEventType.DELETE,
    #             "event_resource": instance.pk,
    #         }
    #     ).data
    # FIX @korchizhinskijna: Delete this notification by email
    from_email = str(DynamicEmailConfiguration.get_solo().from_email)
    to_email = ["drodikova@yandex.ru"]
    subject = "Удаление предложения"
    message = f"""
            "data_type": "OFFERS",
            "event_type": {SignalsEventType.DELETE}
            "event_resource": {instance.pk}
    """
    send_mail(subject, message, from_email, to_email, fail_silently=False)
