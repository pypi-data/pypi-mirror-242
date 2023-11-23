from django.utils import timezone

from des.models import DynamicEmailConfiguration
from django.core.mail import EmailMessage

from config.settings import settings
from modules.core.models import ActiveCitizenModule
from modules.core.models.active_citizen_module import ActiveCitizenModuleEnum

WELCOME_MESSAGE = "Добрый день! Благодарим Вас за участие в проекте."


def send_email(subject, to, body, from_email=None):
    ecology_stimulation_module = ActiveCitizenModule.objects.filter(
        name=ActiveCitizenModuleEnum.ECOLOGY_STIMULATION).first()
    ecology_offers_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.ECOLOGY_OFFERS).first()

    if ecology_stimulation_module and ecology_offers_module:
        bonus_program = ecology_stimulation_module.is_worked and ecology_offers_module.is_worked
    else:
        bonus_program = settings.BONUS_PROGRAM
    if not bonus_program:
        return

    email_configuration = DynamicEmailConfiguration.get_solo()
    if not from_email:
        from_email = str(getattr(email_configuration, "from_email"))
    try:
        msg = EmailMessage(
            subject=subject,
            from_email=from_email,
            to=to,
            body=body,
        )

        msg.send(fail_silently=True)
    except Exception as e:
        print(f"5. {e}")
        err = EmailMessage(
            subject="Ошибка",
            from_email=str(getattr(email_configuration, "from_email", None)),
            to=["shahovrs@cifra-k.ru"],
            body=f"5. {e}",
        )
        err.send(fail_silently=False)

    return None


def send_email_on_participation_event(
        to, event_name, reward, from_email=None, welcome_message=WELCOME_MESSAGE
):
    body = (
        f"{welcome_message}\n"
        f"Предложение: {event_name}\n"
        f"Количество начисленных бонусов: {reward}\n"
        f"Дата: {timezone.localdate()} "
        f'{timezone.localtime().strftime("%H:%M:%S")}\n'
        f"Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru/"
    )

    send_email(
        subject="Участие в мероприятии",
        from_email=from_email,
        to=to,
        body=body,
    )


def send_email_on_purchase_confirm(
        to, reward_name, cost, from_email=None, welcome_message=WELCOME_MESSAGE
):
    body = (
        f"{welcome_message}\n"
        f"Поощрение: {reward_name}\n"
        f"Количество списанных бонусов: {cost} бонусов\n"
        f"Дата: {timezone.localdate()} "
        f'{timezone.localtime().strftime("%H:%M:%S")}\n'
        f"Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru/"
    )

    send_email(
        subject="Подтверждение получения поощрения",
        from_email=from_email,
        to=to,
        body=body,
    )


def send_email_on_participation_vote(
        to, vote_name, reward, from_email=None, welcome_message=WELCOME_MESSAGE
):
    body = (
        f"{welcome_message}\n"
        f"Голосование: {vote_name}\n"
        f"Количество начисленных бонусов: {reward}\n"
        f"Дата: {timezone.localdate()} "
        f'{timezone.localtime().strftime("%H:%M:%S")}\n'
        f"Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru/"
    )

    send_email(
        subject="Участие в голосовании",
        from_email=from_email,
        to=to,
        body=body,
    )


def send_email_on_user_adding_initiative(
        to, initiative_name, reward, from_email=None, welcome_message=WELCOME_MESSAGE
):
    body = (
        f"{welcome_message}\n"
        f"Инициатива: {initiative_name}\n"
        f"Количество начисленных бонусов: {reward}\n"
        f"Дата: {timezone.localdate()} "
        f'{timezone.localtime().strftime("%H:%M:%S")}\n'
        f"Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru/"
    )

    send_email(
        subject="Подача инициативы",
        from_email=from_email,
        to=to,
        body=body,
    )


def send_email_on_user_approve_initiative(
        to, initiative_name, reward, from_email=None, welcome_message=WELCOME_MESSAGE
):
    body = (
        f"{welcome_message}\n"
        f"Инициатива: {initiative_name}\n"
        f"Количество начисленных бонусов: {reward}\n"
        f"Дата: {timezone.localdate()} "
        f'{timezone.localtime().strftime("%H:%M:%S")}\n'
        f"Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru/"
    )

    send_email(
        subject="Поддержка инициативы",
        from_email=from_email,
        to=to,
        body=body,
    )


def send_email_on_ecology_participation(
        to, reward, from_email=None, welcome_message=WELCOME_MESSAGE
):
    body = (
        f"{welcome_message}\n"
        f"Количество начисленных бонусов: {reward}\n"
        f"Дата: {timezone.localdate()} "
        f'{timezone.localtime().strftime("%H:%M:%S")}\n'
        f"Для просмотра подробной информации перейдите в личный кабинет http://24ag.ru/"
    )

    send_email(
        subject="Участие в программе",
        from_email=from_email,
        to=to,
        body=body,
    )
