from django.conf import settings
from django.db import models


class UserVote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    vote = models.ForeignKey(
        "voting.Vote",
        on_delete=models.CASCADE,
        verbose_name="Голосование",
    )
    question = models.ForeignKey(
        "voting.VoteQuestion",
        on_delete=models.CASCADE,
        verbose_name="Вопрос голосования",
    )
    answer_option = models.ForeignKey(
        to="voting.VoteAnswerOption",
        on_delete=models.CASCADE,
        verbose_name="Вариант ответа",
        blank=True,
        null=True,
    )
    custom_answer = models.TextField(
        verbose_name="Вариант пользоваьеля",
        blank=True,
        null=True,
    )
    locality = models.ForeignKey(
        to="core.Locality",
        verbose_name="Муниципальное образование",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        indexes = [
            models.Index(fields=["user", "vote"]),
            models.Index(fields=["user", "vote", "question"]),
        ]
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"
