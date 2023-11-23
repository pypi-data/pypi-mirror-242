from des.models import DynamicEmailConfiguration
from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from modules.ecology.models.user_profile import UserProfile

from modules.integration.enums.signals_event_type import SignalsEventType
from modules.integration.services.signals_serializer import SignalSerializer
from modules.integration.task import send_signal_about_balance


@receiver(pre_save, sender=UserProfile)
def get_instanse_before_save(sender, instance: UserProfile, **kwargs):
    if instance.pk and instance.user.user_synchronization.exists():
        setattr(instance, "_previous_state_instance", sender.objects.get(pk=instance.pk))


@receiver(post_save, sender=UserProfile)
def signaling_for_change_user_balance(sender, instance: UserProfile, **kwargs):
    if previous_instance := getattr(instance, "_previous_state_instance", None):

        # If user balance was changed - send signal with message about this.
        if instance.balance != previous_instance.balance:

            # external_ids = [obj.external_system_id for obj in instance.user_synchronization.all()]
            # data = {
            #     "data_type": "BALANCE",
            #     "event_type": SignalsEventType.UPDATE,
            #     "event_resource": instance.pk,
            # }
        # FIX @korchizhinskijna: Delete this notification by email
            from_email = str(DynamicEmailConfiguration.get_solo().from_email)
            to_email = ["drodikova@yandex.ru"]
            subject = "Изменение баланса пользователя"
            message = f"""
                    "data_type": "BALANCE",
                    "event_type": {SignalsEventType.UPDATE}
                    "event_resource": {instance.pk}
            """
            send_mail(subject, message, from_email, to_email, fail_silently=False)

            # send_signal_about_balance.delay(data=SignalSerializer(data).data, external_ids=external_ids)
