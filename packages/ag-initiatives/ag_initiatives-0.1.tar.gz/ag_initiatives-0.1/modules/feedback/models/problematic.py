from django.db import models


class Problematic(models.Model):
    name = models.CharField(
        verbose_name="Название", null=True, default=None, max_length=600
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Проблематика"
        verbose_name_plural = "Проблематики"

        indexes = [
            models.Index(
                fields=[
                    "id",
                ]
            ),
        ]
