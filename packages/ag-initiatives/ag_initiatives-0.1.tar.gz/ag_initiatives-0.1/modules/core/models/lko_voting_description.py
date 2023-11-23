import collections

from django.db import models
from modules.core.enum import VotingType


class LkoVotingDescription(models.Model):
    description_id = models.TextField(
        verbose_name="Идентификатор описания",
    )
    text = models.TextField(
        verbose_name="Текст",
        blank=True,
    )
    voting_type = models.CharField(
        verbose_name="Тип голосования",
        max_length=15,
        unique=True,
        choices=VotingType.CHOICES,
    )

    def __str__(self):
        return self.description_id

    class Meta:
        verbose_name = 'Описание механизма проведения голосований'
        verbose_name_plural = 'Описания механизмов проведения голосований'
