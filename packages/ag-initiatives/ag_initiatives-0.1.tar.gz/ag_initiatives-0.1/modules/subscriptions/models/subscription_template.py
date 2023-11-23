from django.db import models

from modules.subscriptions.enums import EventEnum


class SubscriptionTemplate(models.Model):
    """Модель: Шаблон письма"""

    class Meta:
        verbose_name = "Шаблон письма"
        verbose_name_plural = "Шаблоны писем"

    title = models.CharField(
        verbose_name="Заголовок",
        max_length=1000,
        help_text="Для указания события используйте указатель `{event}`",
    )
    body = models.TextField(
        verbose_name="Тело письма",
        help_text="Указатели: "
        "`{event}` - событие; "
        "`{user}` - ФИО пользователя; "
        "`{category}` - категория; "
        "`{locality}` - населённый пункт; "
        "`{date}` - дата события; "
        "`{time}` - время события",
    )
    event_type = models.CharField(
        verbose_name="Тип события",
        choices=EventEnum.TYPE_CHOICES,
        default=None,
        null=True,
        blank=True,
        max_length=255,
    )

    def __str__(self):
        return self.title
