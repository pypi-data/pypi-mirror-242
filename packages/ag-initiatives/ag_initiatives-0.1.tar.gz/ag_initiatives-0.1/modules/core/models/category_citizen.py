from django.db import models


class CategoryCitizen(models.Model):
    """
    Категория гражданина.
    Пример "Молодежь"
    """

    name = models.TextField(verbose_name="Категория гражданина")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория гражданина"
        verbose_name_plural = "Категории граждан"

        ordering = ["name"]
