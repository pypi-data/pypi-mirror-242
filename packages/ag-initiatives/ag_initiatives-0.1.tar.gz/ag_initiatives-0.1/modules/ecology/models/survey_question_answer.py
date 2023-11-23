from django.db import models


class SurveyQuestionAnswer(models.Model):
    question = models.ForeignKey(
        to="ecology.SurveyQuestion",
        verbose_name="Вопрос анкеты",
        related_name="answers",
        on_delete=models.CASCADE,
    )

    text = models.TextField(
        verbose_name="Текст",
    )

    group = models.TextField(
        verbose_name="Группа",
        blank=True,
        null=True,
    )

    order = models.PositiveIntegerField(
        verbose_name="Порядок",
        default=0,
    )

    def __str__(self):
        return self.text[: max(16, len(self.text))]

    class Meta:
        verbose_name = "Вариант ответа на вопрос анкеты"
        verbose_name_plural = "Варианты ответов на вопросы анкет"
