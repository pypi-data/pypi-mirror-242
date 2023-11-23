from django.conf import settings
from django.db import models


class UserMunicipalVote(models.Model):
    """
    Отчёт по муниципальному голосованию конкретного пользователя.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    vote = models.ForeignKey(
        "voting.VoteMunicipal",
        on_delete=models.CASCADE,
        verbose_name="Мунициальное голосование",
        null=True,
        blank=True,
    )
    vote_reg = models.ForeignKey(
        "voting.Voteregional",
        on_delete=models.CASCADE,
        verbose_name="Региональное голосование",
        null=True,
        blank=True,
    )
    vote_loc = models.ForeignKey(
        "voting.Votelocal",
        on_delete=models.CASCADE,
        verbose_name="Локальное голосование",
        null=True,
        blank=True,
    )
    question = models.ForeignKey(
        "voting.VoteMunicipalQuestion",
        on_delete=models.CASCADE,
        verbose_name="Вопрос муниципального голосования",
        null=True,
        blank=True,
    )
    question_reg = models.ForeignKey(
        "voting.VoteRegionalQuestion",
        on_delete=models.CASCADE,
        verbose_name="Вопрос регионального голосования",
        null=True,
        blank=True,
    )
    question_loc = models.ForeignKey(
        "voting.VoteLocalQuestion",
        on_delete=models.CASCADE,
        verbose_name="Вопрос локального голосования",
        null=True,
        blank=True,
    )
    answer_option = models.ForeignKey(
        to="voting.VoteMunicipalAnswer",
        on_delete=models.CASCADE,
        verbose_name="Вариант муниципального ответа",
        blank=True,
        null=True,
    )
    answer_reg = models.ForeignKey(
        to="voting.VoteRegionalAnswer",
        on_delete=models.CASCADE,
        verbose_name="Вариант регионального ответа",
        blank=True,
        null=True,
    )
    answer_loc = models.ForeignKey(
        to="voting.VoteLocalAnswer",
        on_delete=models.CASCADE,
        verbose_name="Вариант локального ответа",
        blank=True,
        null=True,
    )
    custom_answer = models.TextField(
        verbose_name="Вариант пользователя",
        blank=True,
        null=True,
    )
    locality = models.ForeignKey(
        to="core.Locality",
        verbose_name="Населенный пункт",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    municipality = models.ForeignKey(
        to="core.Municipality",
        verbose_name="Муниципальный округ",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name= "municipality"
    )
    local_groups = models.ForeignKey(
        to="voting.LocalVotingGroup",
        verbose_name="Локальная группа",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name= "local_group"
    )

    class Meta:
        indexes = [
            models.Index(fields=["user", "vote"]),
            models.Index(fields=["user", "vote", "question"]),
        ]
        verbose_name = "Ответ пользователя по муниципальному голосованию"
        verbose_name_plural = "Ответы пользователей по муниципальным голосованиям"
