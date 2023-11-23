from des.models import DynamicEmailConfiguration

from modules.core.models import user
from modules.initiatives.tasks import (
    send_email_on_initiative_state_change,
    send_email_initiative_broadcast,
)
from modules.initiatives.utils.mail_strings import EmailString


class EmailBuilder:
    def __init__(
        self,
        initiative,
        user_template_string=None,
        operator_template_string=None,
        role_broadcast_template_string=None,
        subject=None,
    ):
        self.initiative = initiative
        self.user = initiative.user
        self.template_string = user_template_string
        self.operator_template_string = operator_template_string
        self.role_broadcast_template_string = role_broadcast_template_string
        self.subject = subject

    def build(self):
        return {
            "subject": f"Здравствуйте, {self.user.first_name} {self.user.patronymic_name}!",
            "from_mail": str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            "to_mail": self.initiative.email,
            "text": self.template_string.format(
                self.initiative.number,
                self.initiative.title,
            ),
        }

    def build_for_department(self):
        return {
            "subject": self.subject if self.subject else self.initiative.number,
            "from_mail": str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            "to_mail": self.initiative.settings.department.email,
            "text": self.operator_template_string.format(
                self.initiative.number, self.initiative.title
            ),
        }

    def build_role_broadcast(self, role: str):
        """Рассылка по роли"""
        users = user.User.objects.filter(roles__contains=role)
        broadcast_emails = list(users.values_list("work_email", flat=True).distinct())
        return {
            "subject": "Новая инициатива на портале «Активный гражданин»",
            "from_mail": str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            "to_mail": broadcast_emails,
            "text": self.role_broadcast_template_string.format(
                self.initiative.number, self.initiative.title
            ),
        }


class EmailSender:
    def __init__(self, builder: EmailBuilder):
        self.builder = builder

    def send_to_user_if_notifications_enabled(self):
        if self.user_notifications_enabled:
            send_email_on_initiative_state_change.apply_async(
                kwargs=self.builder.build()
            )

    def send_to_department_if_notifications_enabled(self):
        if self.department_notifications_enabled:
            send_email_on_initiative_state_change.apply_async(
                kwargs=self.builder.build_for_department()
            )

    def send_role_broadcast(self, role: str):
        send_email_initiative_broadcast.apply_async(
            kwargs=self.builder.build_role_broadcast(role)
        )

    @property
    def user_notifications_enabled(self):
        return self.builder.user.email_initiative_notification

    @property
    def department_notifications_enabled(self):
        return self.builder.initiative.settings.department.email_initiative_notification

    def send_operator_broadcast_with_department(self, initiative):
        operators = user.User.objects.filter(roles__icontains=user.UserRole.OPERATOR)
        operators_for_broadcast = operators.filter(
            department=initiative.settings.department,
            email_initiative_notification=True,
        )
        broadcast_emails = list(operators_for_broadcast.values_list("work_email", flat=True).distinct())
        mail_content = {
            "subject": "Новая инициатива на портале «Активный гражданин»",
            "from_mail": str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            "to_mail": broadcast_emails,
            "text": EmailString.PREMODERATION_ACCEPTED_OPERATOR.format(
                initiative.number, initiative.title
            ),
        }

        send_email_initiative_broadcast.apply_async(kwargs=mail_content)
