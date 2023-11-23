from django.db import models


class Feedback(models.Model):
    first_name = models.TextField(
        verbose_name="Имя",
    )
    last_name = models.TextField(
        verbose_name="Фамилия",
    )
    patronymic_name = models.TextField(
        verbose_name="Отчество",
    )
    email = models.EmailField(
        verbose_name="email",
    )
    phone = models.TextField(
        verbose_name="Номер телефона",
    )
    comment = models.TextField(
        verbose_name="Отзыв",
    )
    file = models.FileField(
        verbose_name="Файл",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Отзыв {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.patronymic_name}"

    @property
    def piece_of_comment(self):
        return f"{self.comment[:70]}..."

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"
