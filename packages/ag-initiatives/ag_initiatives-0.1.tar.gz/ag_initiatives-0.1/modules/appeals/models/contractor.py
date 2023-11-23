from django.db import models


class Contractor(models.Model):
    name = models.TextField(verbose_name="Наименование")
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        blank=True,
        null=True,
    )
    locality = models.ManyToManyField(
        to="core.Locality",
        verbose_name="Муниципальные образования",
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"
