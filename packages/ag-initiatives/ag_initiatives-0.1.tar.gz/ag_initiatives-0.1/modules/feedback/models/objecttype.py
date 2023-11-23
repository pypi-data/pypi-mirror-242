from django.db import models


class ObjectType(models.Model):
    name = models.CharField(
        verbose_name="Название", null=True, default=None, max_length=255
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип объекта"
        verbose_name_plural = "Типы объектов"

        indexes = [
            models.Index(
                fields=[
                    "id",
                ]
            ),
        ]
