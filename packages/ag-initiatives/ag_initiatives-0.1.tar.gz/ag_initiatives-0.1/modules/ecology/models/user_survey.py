from django.conf import settings
from django.db import models


class UserSurvey(models.Model):
    user = models.ForeignKey(
        to="core.User",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    survey = models.ForeignKey(
        "ecology.Survey",
        on_delete=models.CASCADE,
        verbose_name="Анкета",
    )

    question = models.ForeignKey(
        "ecology.SurveyQuestion",
        on_delete=models.CASCADE,
        verbose_name="Вопрос",
    )

    answer = models.ForeignKey(
        to="ecology.SurveyQuestionAnswer",
        on_delete=models.CASCADE,
        verbose_name="Вариант ответа",
    )

    timestamp = models.DateTimeField(
        verbose_name="Дата-время",
    )

    class Meta:
        indexes = [
            models.Index(fields=["user", "survey"]),
            models.Index(fields=["user", "survey", "question"]),
        ]
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"
