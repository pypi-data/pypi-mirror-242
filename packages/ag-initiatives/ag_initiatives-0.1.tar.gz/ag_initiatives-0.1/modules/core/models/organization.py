from django.db import models


class Organization(models.Model):
    name = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация бонусной программы"
        verbose_name_plural = "Организации бонусной программы"
