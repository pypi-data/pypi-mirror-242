from django.db import models


class DeletionNotification(models.Model):
    """ Модель оповещения об удалении учётной записи."""
    header = models.TextField(verbose_name="Заголовок")
    text = models.TextField(
        max_length=500,
        verbose_name="Текст",
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Оповещение об удалении учётной записи"
        verbose_name_plural = "Оповещения об удалении учётной записи"
