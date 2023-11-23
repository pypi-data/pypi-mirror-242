from celery.utils.log import get_task_logger
from django.utils import timezone
from des.models import DynamicEmailConfiguration

from modules.voting.models import Vote, VoteState, VoteMunicipal, VoteRegional, VoteLocal, LocalVotingGroup
from config.settings.celery import app

from ..task import send_email_on_vote_state_change, send_email_on_local_vote_created
from ...core.models import User, UserRole

EMAIL_CONTENT__OPERATOR__MODERATION_ACCEPTED = """
Здравствуйте!
Ваше голосование «{}» согласовано для публикации на цифровой платформе «Активный гражданин» https://24ag.ru/.
Вам необходимо перейти в личный кабинет для публикации опроса.

С уважением, 
Цифровая платформа «Активный гражданин»
https://24ag.ru/
"""

EMAIL_CONTENT__OPERATOR__MODERATION_ACCEPTED__WITH__CHANGES = """Голосование "{}" прошло модерацию. Модератором внесены изменения в форму голосования.
Подтвердите публикацию голосования на Портале.
Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru.
"""

EMAIL_CONTENT__OPERATOR__MODERATION_REJECTED = """
Здравствуйте!
Ваше голосование «{}» отклонено для публикации на цифровой платформе «Активный гражданин» https://24ag.ru/.

С уважением, 
Цифровая платформа «Активный гражданин»
https://24ag.ru/
"""

EMAIL_CONTENT__OPERATOR__PUBLISHED = """На Портале «Активный гражданин. Красноярский край» открыто голосование "{}".
Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru.
"""

EMAIL_CONTENT__OPERATOR__FINISHED = """На Портале «Активный гражданин. Красноярский край» завершено голосование "{}".
Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru.
"""

EMAIL_CONTENT__MODERATOR__VOTE_CREATED = """
Здравствуйте!
На цифровой платформе «Активный гражданин» размещено новое голосование «{}».
Инициатор голосования: {}.
Период голосования: {} - {}.
Пожалуйста, авторизуйтесь на портале https://24ag.ru/ с помощью учетной записи Госуслуг. Перейдите в личный кабинет и проверьте голосование на корректность: отредактируйте, согласуйте или отклоните его.

С уважением, 
Цифровая платформа «Активный гражданин»
https://24ag.ru/
"""

EMAIL_CONTENT__LOCAL_VOTE__CREATED = """
Здравствуйте!
На цифровой платформе «Активный гражданин» размещено новое голосование «{}».
Инициатор голосования: {}.
Период голосования: до: {}.
Пожалуйста, авторизуйтесь на портале https://24ag.ru/ с помощью учетной записи Госуслуг. Перейдите в личный кабинет и проверьте голосование на корректность: отредактируйте, согласуйте или отклоните его.

С уважением, 
Цифровая платформа «Активный гражданин»
https://24ag.ru/
"""


class MailService:
    @staticmethod
    def notify_operator__moderation_accepted(vote: Vote):
        if not vote.department or not vote.author:
            return

        operator_work_email = vote.author.work_email

        send_email_on_vote_state_change.delay(
            subject="Голосование на портале «Активный гражданин» согласовано",
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[operator_work_email],
            body=EMAIL_CONTENT__OPERATOR__MODERATION_ACCEPTED.format(vote.name),
        )
        if not vote.department.email_initiative_notification:
            return
        send_email_on_vote_state_change.delay(
            subject=vote.name,
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[vote.department.email],
            body=EMAIL_CONTENT__OPERATOR__MODERATION_ACCEPTED.format(vote.name),
        )

    @staticmethod
    def notify_operator__moderation_accepted__with__changes(vote: Vote):
        if not vote.department or not vote.author:
            return

        operator_work_email = vote.author.work_email

        send_email_on_vote_state_change.delay(
            subject="Голосование на портале «Активный гражданин» согласовано",
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[operator_work_email],
            body=EMAIL_CONTENT__OPERATOR__MODERATION_ACCEPTED__WITH__CHANGES.format(vote.name),
        )

        if not vote.department.email_initiative_notification:
            return

        send_email_on_vote_state_change.delay(
            subject=vote.name,
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[vote.department.email],
            body=EMAIL_CONTENT__OPERATOR__MODERATION_ACCEPTED__WITH__CHANGES.format(vote.name),
        )

    @staticmethod
    def notify_operator__moderation_rejected(vote: Vote):
        if not vote.department or not vote.author:
            return

        operator_work_email = vote.author.work_email

        send_email_on_vote_state_change.delay(
            subject="Голосование на портале «Активный гражданин» отклонено",
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[operator_work_email],
            body=EMAIL_CONTENT__OPERATOR__MODERATION_REJECTED.format(vote.name),
        )

        if not vote.department.email_initiative_notification:
            return

        send_email_on_vote_state_change.delay(
            subject=vote.name,
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[vote.department.email],
            body=EMAIL_CONTENT__OPERATOR__MODERATION_REJECTED.format(vote.name),
        )

    @staticmethod
    def notify_operator__published(vote: Vote):
        if not vote.department or not vote.author:
            return

        operator_work_email = vote.author.work_email

        send_email_on_vote_state_change.delay(
            subject="Голосование на портале «Активный гражданин» открыто",
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[operator_work_email],
            body=EMAIL_CONTENT__OPERATOR__PUBLISHED.format(vote.name),
        )

        if not vote.department.email_initiative_notification:
            return

        send_email_on_vote_state_change.delay(
            subject=vote.name,
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[vote.department.email],
            body=EMAIL_CONTENT__OPERATOR__PUBLISHED.format(vote.name),
        )

    @staticmethod
    def notify_operator__finished(vote: Vote):
        if not vote.department or not vote.author:
            return

        operator_work_email = vote.author.work_email

        send_email_on_vote_state_change.delay(
            subject="Голосование на портале «Активный гражданин» завершено",
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[operator_work_email],
            body=EMAIL_CONTENT__OPERATOR__FINISHED.format(vote.name),
        )

        if not vote.department.email_initiative_notification:
            return

        send_email_on_vote_state_change.delay(
            subject=vote.name,
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=[vote.department.email],
            body=EMAIL_CONTENT__OPERATOR__FINISHED.format(vote.name),
        )

    @staticmethod
    def notify_moderator__vote_created(vote: Vote):
        if not vote.department:
            return

        moderators = User.objects.filter(
            roles__contains=UserRole.MODERATOR, email__isnull=False
        )
        moderators_emails = list()
        for moderator in moderators:
            moderators_emails.append(moderator.work_email)

        send_email_on_vote_state_change.delay(
            subject="Новое голосование на портале «Активный гражданин»",
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=moderators_emails,
            body=EMAIL_CONTENT__MODERATOR__VOTE_CREATED.format(
                vote.name, vote.department, vote.start_date.strftime('%d.%m.%Y'), vote.end_date.strftime('%d.%m.%Y')
            ),
        )

    @staticmethod
    def notify_participant__local_vote_created(vote: VoteLocal):
        query = vote.participants_groups.prefetch_related("participants")
        lst = []
        for loc_vote in query:
            parts = [p.email for p in loc_vote.participants.all()]
            lst.extend(parts)

        send_email_on_vote_state_change.delay(
            subject="Новое локальное голосование на портале «Активный гражданин»",
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=lst,
            body=EMAIL_CONTENT__LOCAL_VOTE__CREATED.format(
                vote.name, vote.department, vote.end_date.strftime('%d.%m.%Y')
            ),
        )


logger = get_task_logger(__name__)


@app.task
def update_votes_status():
    published = Vote.objects.filter(
        state=VoteState.OPERATOR_ACCEPTED,
        start_date__lte=timezone.now(),
    )

    if published.count() > 0:
        logger.info(f"publish {published.count()} votes")

    for vote in published:
        MailService.notify_operator__published(vote)

    published.update(
        state=VoteState.PUBLISHED,
        is_opened=True,
        is_published=True,
    )

    finished = Vote.objects.filter(
        state=VoteState.PUBLISHED,
        end_date__lte=timezone.now(),
    )

    if finished.count() > 0:
        logger.info(f"finish {finished.count()} votes")

    for vote in finished:
        MailService.notify_operator__finished(vote)

    finished.update(
        state=VoteState.FINISHED,
        is_opened=False,
    )
    #########################################
    published = VoteMunicipal.objects.filter(
        state=VoteState.OPERATOR_ACCEPTED,
        start_date__lte=timezone.now(),
    )

    if published.count() > 0:
        logger.info(f"publish {published.count()} votes")

        for vote in published:
            MailService.notify_operator__published(vote)

        published.update(
            state=VoteState.PUBLISHED,
            is_opened=True,
            is_published=True,
        )

    finished = VoteMunicipal.objects.filter(
        state=VoteState.PUBLISHED,
        end_date__lte=timezone.now(),
    )

    if finished.count() > 0:
        logger.info(f"finish {finished.count()} votes")

        for vote in finished:
            MailService.notify_operator__finished(vote)

        finished.update(
            state=VoteState.FINISHED,
            is_opened=False,
        )
    #######################################
    published = VoteRegional.objects.filter(
        state=VoteState.OPERATOR_ACCEPTED,
        start_date__lte=timezone.now(),
    )

    if published.count() > 0:
        logger.info(f"publish {published.count()} votes")

        for vote in published:
            MailService.notify_operator__published(vote)

        published.update(
            state=VoteState.PUBLISHED,
            is_opened=True,
            is_published=True,
        )

    finished = VoteRegional.objects.filter(
        state=VoteState.PUBLISHED,
        end_date__lte=timezone.now(),
    )

    if finished.count() > 0:
        logger.info(f"finish {finished.count()} votes")

        for vote in finished:
            MailService.notify_operator__finished(vote)

        finished.update(
            state=VoteState.FINISHED,
            is_opened=False,
        )
    ############################################
    published = VoteLocal.objects.filter(
        state=VoteState.OPERATOR_ACCEPTED,
        start_date__lte=timezone.now(),
    )

    if published.count() > 0:
        logger.info(f"publish {published.count()} votes")

        for vote in published:
            MailService.notify_operator__published(vote)
            MailService.notify_participant__local_vote_created(vote)

        published.update(
            state=VoteState.PUBLISHED,
            is_opened=True,
            is_published=True,
        )

    finished = VoteLocal.objects.filter(
        state=VoteState.PUBLISHED,
        end_date__lte=timezone.now(),
    )

    if finished.count() > 0:
        logger.info(f"finish {finished.count()} votes")

        for vote in finished:
            MailService.notify_operator__finished(vote)

        finished.update(
            state=VoteState.FINISHED,
            is_opened=False,
        )
