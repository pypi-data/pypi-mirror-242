from des.models import DynamicEmailConfiguration

from modules.appeals.task import send_email_on_appeal_state_change
from modules.appeals_pos.models import Appeal

EMAIL_CONTENT__USER__MODERATION = """Здравствуйте, {}!
Ваше обращение {} направлено на модерацию.
Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru
"""

EMAIL_CONTENT__USER__MODERATION_ACCEPTED = """Здравствуйте, {}!
Ваше обращение {} прошло предварительную модерацию и направлено на рассмотрение.
Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru
"""


EMAIL_CONTENT__USER__MODERATION_REJECTED = """Здравствуйте, {}!
Ваше обращение {} отклонено по результатам предварительной модерации.
{}
Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru
"""


EMAIL_CONTENT__USER__IN_PROGRESS = """Здравствуйте, {}!
По Вашему обращению {} назначен исполнитель.
Для просмотра подробной информации перейдите по ссылке http://24ag.ru
"""


EMAIL_CONTENT__USER__RESPONDED = """Здравствуйте, {}!
По Вашему обращению {} получен ответ.
Для просмотра подробной информации перейдите по ссылке http://24ag.ru
"""


class MailService:
    def __init__(self, appeal):
        self.appeal: Appeal = appeal

    def notify_user_accepted(self):
        appeal = self.appeal
        if not appeal.user.email_appeals_notification or not appeal.user.email_initiative_notification:
            return

        send_email_on_appeal_state_change.delay(
            subject=appeal.pos_id,
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[appeal.user.email],
            body=EMAIL_CONTENT__USER__MODERATION_ACCEPTED.format(
                f"{appeal.user.first_name} {appeal.user.patronymic_name}",
                f'{appeal.pos_id}',
            ),
        )

    def notify_user_moderation(self):
        appeal = self.appeal
        if not appeal.user.email_appeals_notification or not appeal.user.email_initiative_notification:
            return

        send_email_on_appeal_state_change.delay(
            subject=appeal.pos_id,
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[appeal.user.email],
            body=EMAIL_CONTENT__USER__MODERATION.format(
                f"{appeal.user.first_name} {appeal.user.patronymic_name}",
                f'{appeal.pos_id}',
            ),
        )

    def notify_user_rejected(self, reason_text: str):
        appeal = self.appeal
        if not appeal.user.email_appeals_notification or not appeal.user.email_initiative_notification:
            return

        send_email_on_appeal_state_change.delay(
            subject=appeal.pos_id,
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[appeal.user.email],
            body=EMAIL_CONTENT__USER__MODERATION_REJECTED.format(
                f"{appeal.user.first_name} {appeal.user.patronymic_name}",
                f'{appeal.pos_id}',
                reason_text,
            ),
        )

    def notify_user_in_progress(self):
        appeal = self.appeal
        if not appeal.user.email_appeals_notification or not appeal.user.email_initiative_notification:
            return

        send_email_on_appeal_state_change.delay(
            subject=appeal.pos_id,
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[appeal.user.email],
            body=EMAIL_CONTENT__USER__IN_PROGRESS.format(
                f"{appeal.user.first_name} {appeal.user.patronymic_name}",
                f'{appeal.pos_id}',
            ),
        )

    def notify_user_responded(self):
        appeal = self.appeal
        if not appeal.user.email_appeals_notification or not appeal.user.email_initiative_notification:
            return

        send_email_on_appeal_state_change.delay(
            subject=appeal.pos_id,
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[appeal.user.email],
            body=EMAIL_CONTENT__USER__RESPONDED.format(
                f"{appeal.user.first_name} {appeal.user.patronymic_name}",
                f'{appeal.pos_id}',
            ),
        )

