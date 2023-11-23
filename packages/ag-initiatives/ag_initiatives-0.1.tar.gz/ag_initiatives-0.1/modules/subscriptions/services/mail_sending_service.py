from typing import List, Dict

from des.models import DynamicEmailConfiguration
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend

from modules.subscriptions.enums import EventEnum
from modules.subscriptions.models import NotificationSendingLog


class EmailBackendService(EmailBackend):
    """Сервис отправки писем"""

    email_configuration = DynamicEmailConfiguration.get_solo()
    EMAIL_HOST: str = email_configuration.host
    EMAIL_PORT: int = email_configuration.port
    EMAIL_HOST_USER: str = email_configuration.from_email
    EMAIL_HOST_PASSWORD: str = email_configuration.password
    EMAIL_USE_TLS: bool = True
    EMAIL_USE_SSL: bool = False

    def __init__(self, **kwargs: object) -> None:
        """
        Инициализация объекта
        """
        kwargs["host"] = self.EMAIL_HOST
        kwargs["port"] = self.EMAIL_PORT
        kwargs["from_email"] = self.EMAIL_HOST_USER
        kwargs["username"] = self.EMAIL_HOST_USER
        kwargs["password"] = self.EMAIL_HOST_PASSWORD
        kwargs["use_tls"] = self.EMAIL_USE_TLS
        kwargs["use_ssl"] = self.EMAIL_USE_SSL
        super().__init__(**kwargs)

    def _format_body(self, task: NotificationSendingLog) -> str:
        """Форматирование тела письма по данным задачи"""
        text = task.subscription.template.body
        format_kwargs = self._format_text(task, text)
        return text.format(**format_kwargs)

    @classmethod
    def _format_text(cls, task: NotificationSendingLog, text: str) -> Dict:
        """Форматирование текста"""
        user = f"{task.subscription.user}"
        event = EventEnum.get(task.subscription.event)
        category = f"{task.subscription.category_value}"
        locality = f"{task.subscription.locality}"
        date = task.timestamp.astimezone().date().isoformat()
        time = task.timestamp.astimezone().time().strftime("%H:%M")
        format_kwargs = {}
        if "{user}" in text:
            format_kwargs["user"] = user
        if "{event}" in text:
            format_kwargs["event"] = event
        if "{category}" in text:
            format_kwargs["category"] = category
        if "{locality}" in text:
            format_kwargs["locality"] = locality
        if "{date}" in text:
            format_kwargs["date"] = date
        if "{time}" in text:
            format_kwargs["time"] = time
        return format_kwargs

    def _format_title(self, task: NotificationSendingLog) -> str:
        """Форматирование заголовка письма по данным задачи"""
        text = task.subscription.template.title
        format_kwargs = self._format_text(task, text)
        return text.format(**format_kwargs)

    def message(self, task: NotificationSendingLog) -> EmailMessage:
        """Формирование сообщения из задачи"""
        email_message = EmailMessage(
            self._format_title(task),
            self._format_body(task),
            f"{self.EMAIL_HOST_USER}",
            [task.subscription.user.email],
            reply_to=[f"{self.EMAIL_HOST_USER}"],
            headers={"Message-ID": task.id},
        )
        email_message.content_subtype = "html"
        return email_message

    def send(self, message: EmailMessage):
        """Отправка сообщения"""
        return self.send_messages([message])

    def send_many(self, messages: List[EmailMessage]):
        """Отправка списка сообщений"""
        return self.send_messages(messages)
