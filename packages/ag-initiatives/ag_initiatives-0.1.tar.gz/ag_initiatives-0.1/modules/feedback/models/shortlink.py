import random

from django.db import models
from django.utils import timezone


class ShortLink(models.Model):
    short_key = models.CharField(
        verbose_name="Короткий ключ", null=True, blank=True, unique=True, max_length=10
    )

    full_link = models.TextField(
        verbose_name="Ссылка",
        max_length=1500,
        null=True,
        blank=True,
    )

    active = models.BooleanField(
        verbose_name="Активная", null=True, blank=True, default=True
    )

    validity_period = models.DateField(
        verbose_name="Срок действия",
        default=timezone.datetime(2050, 1, 1).astimezone().date(),
    )

    counter = models.IntegerField(verbose_name="Счётчик", default=0)

    def __str__(self):
        return f"{self.short_key}"

    def generate_short_key(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        min_length = 5
        max_length = 10
        short_key = "".join(
            [
                [
                    alphabet[random.randint(0, len(alphabet) - 1)],
                    alphabet[random.randint(0, len(alphabet) - 1)].upper(),
                ][random.randint(0, 1)]
                for _ in range(min_length, max_length + 1)
            ]
        )
        return short_key

    def set_short_key(self, link=""):
        short_key = self.generate_short_key()
        all = ShortLink.objects.all()
        # print(all.count())
        while all.filter(short_key=short_key).count() > 0:
            short_key = self.generate_short_key()
            all = ShortLink.objects.all()
        self.short_key = short_key
        self.full_link = link
        return short_key

    class Meta:
        verbose_name = "Короткая ссылка"
        verbose_name_plural = "Короткие ссылки"

        indexes = [
            models.Index(fields=["id", "short_key"]),
        ]
