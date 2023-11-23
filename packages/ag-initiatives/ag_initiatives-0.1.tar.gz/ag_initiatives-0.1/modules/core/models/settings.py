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


class Settings(SingletonModel):
    privacy_policy = models.TextField(
        verbose_name="Политика использования персональных данных", blank=True, null=True
    )

    def __str__(self):
        return "Текстовые настройки"

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"
