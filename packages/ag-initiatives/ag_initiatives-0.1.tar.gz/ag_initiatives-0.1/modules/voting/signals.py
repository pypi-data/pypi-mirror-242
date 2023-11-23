import logging
from des.models import DynamicEmailConfiguration
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from modules.integration.enums.signals_event_type import SignalsEventType
from modules.integration.services.signals_serializer import SignalSerializer
from modules.integration.task import send_signal_for_api

from modules.voting.models.vote import Vote


logger = logging.getLogger("integration.signals")


@receiver(pre_save, sender=Vote)
def get_instanse_before_save(sender, instance: Vote, **kwargs):
    if instance.pk:
        setattr(instance, "_previous_state_instance", sender.objects.get(pk=instance.pk))


@receiver(post_save, sender=Vote)
def signaling_for_create_vote(sender, instance: Vote, **kwargs):
    if previous_instance := getattr(instance, "_previous_state_instance", None):

        # If vote was unpublished - send signal with message about this.
        if instance.is_published and not previous_instance.is_published:

            # send_signal_for_api.delay(data=SignalSerializer({
            #     "data_type": "VOTING",
            #     "event_type": SignalsEventType.PUBLISH,
            #     "event_resource": instance.pk,
            # }).data)
            # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Публикация голосования"
            message = f"""
                    "data_type": "VOTING",
                    "event_type": {SignalsEventType.PUBLISH}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=True)

        # If vote was published - send signal with message about publishing.
        elif not instance.is_published and previous_instance.is_published:

            # send_signal_for_api.delay(data=SignalSerializer({
            #     "data_type": "VOTING",
            #     "event_type": SignalsEventType.UNPUBLISH,
            #     "event_resource": instance.pk,
            # }).data)
            # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Снятие с публикации голосования"
            message = f"""
                    "data_type": "VOTING",
                    "event_type": {SignalsEventType.UNPUBLISH}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=True)

        # Send message, that vote was changed.
        else:

            # send_signal_for_api.delay(data=SignalSerializer({
            #     "data_type": "VOTING",
            #     "event_type": SignalsEventType.UPDATE,
            #     "event_resource": instance.pk,
            # }).data)
            # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Изменение голосования"
            message = f"""
                    "data_type": "VOTING",
                    "event_type": {SignalsEventType.UPDATE}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=True)

    else:

        # send_signal_for_api.delay(data=SignalSerializer({
        #     "data_type": "VOTING",
        #     "event_type": SignalsEventType.CREATE,
        #     "event_resource": instance.pk,
        # }).data)
        # FIX @korchizhinskijna: Delete this notification by email
        from_email = str(DynamicEmailConfiguration.get_solo().from_email)
        to_email = ["drodikova@yandex.ru"]
        subject = "Создание голосования"
        message = f"""
                "data_type": "VOTING",
                "event_type": {SignalsEventType.CREATE}
                "event_resource": {instance.pk}
        """
        send_mail(subject, message, from_email, to_email, fail_silently=True)


@receiver(post_delete, sender=Vote)
def signaling_for_delete_vote(
    sender, instance: Vote, **kwargs
):

    # send_signal_for_api.delay(data=SignalSerializer({
    #     "data_type": "VOTING",
    #     "event_type": SignalsEventType.DELETE,
    #     "event_resource": instance.pk,
    # }).data)
        # FIX @korchizhinskijna: Delete this notification by email
    from_email = str(DynamicEmailConfiguration.get_solo().from_email)
    to_email = ["drodikova@yandex.ru"]
    subject = "Удаление голосования"
    message = f"""
            "data_type": "VOTING",
            "event_type": {SignalsEventType.DELETE}
            "event_resource": {instance.pk}
    """
    send_mail(subject, message, from_email, to_email, fail_silently=True)
