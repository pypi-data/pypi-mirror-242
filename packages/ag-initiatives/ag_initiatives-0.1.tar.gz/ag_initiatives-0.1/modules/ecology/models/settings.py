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
    participation_reward = models.PositiveIntegerField(
        default=50,
        verbose_name="Награда за участие в проекте",
    )

    survey_reward = models.PositiveIntegerField(
        default=50,
        verbose_name="Награда за заполнение анкеты",
    )

    add_initiative_reward = models.PositiveIntegerField(
        default=50,
        verbose_name="Награда за предложение инициативы",
    )

    approve_initiative_reward = models.PositiveIntegerField(
        default=50, verbose_name="Награда за поддержку инициативы"
    )

    vote_reward = models.PositiveIntegerField(
        default=50, verbose_name="Награда за участие в голосовании"
    )

    status_instruction = models.TextField(
        max_length=500,
        null=True,
        blank=False,
        verbose_name="Инструкция для повышения статуса",
    )

    module_information = models.TextField(
        max_length=500,
        null=True,
        blank=False,
        verbose_name="Описание программы «Система поощрений»",
    )

    min_beginner_bonuses = models.PositiveIntegerField(
        default=0, verbose_name=f'Минимальное количество бонусов для статуса "Новичок"'
    )

    max_beginner_bonuses = models.PositiveIntegerField(
        default=299,
        verbose_name=f'Максимальное количество бонусов для статуса "Новичок"',
    )

    min_dweller_bonuses = models.PositiveIntegerField(
        default=300, verbose_name=f'Минимальное количество бонусов для статуса "Житель"'
    )

    max_dweller_bonuses = models.PositiveIntegerField(
        default=999,
        verbose_name=f'Максимальное количество бонусов для статуса "Житель"',
    )

    min_city_expert_bonuses = models.PositiveIntegerField(
        default=1000,
        verbose_name=f'Минимальное количество бонусов для статуса "Городской эксперт"',
    )

    max_city_expert_bonuses = models.PositiveIntegerField(
        default=2999,
        verbose_name=f'Максимальное количество бонусов для статуса "Городской эксперт"',
    )

    min_active_citizen_bonuses = models.PositiveIntegerField(
        default=3000,
        verbose_name=f'Минимальное количество бонусов для статуса "Активный гражданин"',
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
