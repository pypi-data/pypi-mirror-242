from django.db import models


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(
        to="ecology.Survey",
        verbose_name="Анкета",
        related_name="questions",
        on_delete=models.CASCADE,
    )

    text = models.TextField(
        verbose_name="Текст",
    )

    order = models.PositiveIntegerField(
        verbose_name="Порядок",
        default=0,
    )

    def __str__(self):
        return self.text[: max(16, len(self.text))]

    class Meta:
        verbose_name = "Вопрос анкеты"
        verbose_name_plural = "Вопросы анкет"
