from des.models import DynamicEmailConfiguration
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from modules.initiatives.models.initiative import Initiative
from modules.integration.enums.signals_event_type import SignalsEventType
from modules.integration.services.signals_serializer import SignalSerializer
from modules.integration.task import send_signal_for_api


@receiver(pre_save, sender=Initiative)
def get_instanse_before_save(sender, instance: Initiative, **kwargs):
    if instance.pk:
        setattr(instance, "_previous_state_instance", sender.objects.get(pk=instance.pk))


@receiver(post_save, sender=Initiative)
def signaling_for_create_initiative(sender, instance: Initiative, **kwargs):
    if previous_instance := getattr(instance, "_previous_state_instance", None):

        # If vote was unpublished - send signal with message about this.
        if instance.state != "REJECTED" and previous_instance.state == "REJECTED":

            # send_signal_for_api.delay(data=SignalSerializer({
            #     "data_type": "INITIATIVES",
            #     "event_type": SignalsEventType.PUBLISH,
            #     "event_resource": instance.pk,
            # }).data)
        # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Публикация инициативы"
            message = f"""
                    "data_type": "INITIATIVES",
                    "event_type": {SignalsEventType.PUBLISH}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=False)

        # If vote was published - send signal with message about publishing.
        elif instance.state == "REJECTED" and previous_instance.state != "REJECTED":

            # send_signal_for_api.delay(data=SignalSerializer({
            #     "data_type": "INITIATIVES",
            #     "event_type": SignalsEventType.UNPUBLISH,
            #     "event_resource": instance.pk,
            # }).data)
        # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Снятие с публикации инициативы"
            message = f"""
                    "data_type": "INITIATIVES",
                    "event_type": {SignalsEventType.UNPUBLISH}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=False)

        # Send message, that message was changed.
        else:

            # send_signal_for_api.delay(data=SignalSerializer({
            #     "data_type": "INITIATIVES",
            #     "event_type": SignalsEventType.UPDATE,
            #     "event_resource": instance.pk,
            # }).data)
        # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Изменение инициативы"
            message = f"""
                    "data_type": "INITIATIVES",
                    "event_type": {SignalsEventType.UPDATE}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=False)

    else:

        # send_signal_for_api.delay(data=SignalSerializer({
        #     "data_type": "INITIATIVES",
        #     "event_type": SignalsEventType.CREATE,
        #     "event_resource": instance.pk,
        # }).data)
        # FIX @korchizhinskijna: Delete this notification by email
        from_email = str(DynamicEmailConfiguration.get_solo().from_email)
        to_email = ["drodikova@yandex.ru"]
        subject = "Создание инициативы"
        message = f"""
                "data_type": "INITIATIVES",
                "event_type": {SignalsEventType.CREATE}
                "event_resource": {instance.pk}
        """
        send_mail(subject, message, from_email, to_email, fail_silently=False)

        
@receiver(post_delete, sender=Initiative)
def signaling_for_delete_initiative(
    sender, instance: Initiative, **kwargs
):

    # send_signal_for_api.delay(data=SignalSerializer({
    #     "data_type": "INITIATIVES",
    #     "event_type": SignalsEventType.DELETE,
    #     "event_resource": instance.pk,
    # }).data)
    from_email = str(DynamicEmailConfiguration.get_solo().from_email)
    to_email = ["drodikova@yandex.ru"]
    subject = "Удаление инициативы"
    message = f"""
            "data_type": "INITIATIVES",
            "event_type": {SignalsEventType.DELETE}
            "event_resource": {instance.pk}
    """
    send_mail(subject, message, from_email, to_email, fail_silently=False)
