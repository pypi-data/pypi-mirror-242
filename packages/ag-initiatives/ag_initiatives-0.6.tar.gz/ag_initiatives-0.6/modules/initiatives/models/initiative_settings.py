from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class InitiativeSettings(SingletonModel):
    user_locality_check = models.BooleanField(
        default=True,
        verbose_name="Проверять адрес пользователя при подаче/поддержке инициативы",
    )

    def __str__(self):
        return "Настройки"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"
