from des.models import DynamicEmailConfiguration
from django.db.models.signals import post_save
from django.dispatch import receiver

from modules.core.models import User, UserRole
from modules.initiatives.tasks import send_email_initiative_broadcast
from modules.initiatives.utils.mail_strings import EmailString
from modules.plans.models import PlanComment


@receiver(post_save, sender=PlanComment)
def plan_comment_signal(sender, instance, created, **kwargs):
    if not created:
        return instance

    # Уведомить модераторов о новом сообщении
    users = User.objects.filter(roles__icontains=UserRole.MODERATOR)
    broadcast_emails = list(users.values_list("work_email", flat=True).distinct())
    message = {
        "subject": f'Новый комментраий! План: {instance.plan.name} [{instance.plan.category}]',
        "from_mail": str(
            getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
        ),
        "to_mail": broadcast_emails,
        "text": EmailString.PLAN_COMMENT_CREATED.format(instance.plan.name, instance.plan.category),
    }
    send_email_initiative_broadcast.apply_async(
        kwargs=message
    )
    return instance
