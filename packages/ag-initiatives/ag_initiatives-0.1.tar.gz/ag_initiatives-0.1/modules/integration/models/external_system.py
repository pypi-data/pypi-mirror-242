import binascii
import os

from django.contrib.auth.models import Permission
from django.db import models
from django.db.models.fields import TextField


class CustomPermission(Permission):
    class Meta:
        proxy = True

    def __str__(self):
        return self.name


class ExternalSystemToken(models.Model):
    key = models.CharField(
        verbose_name="ключ (токен)", max_length=40, primary_key=True, blank=True
    )
    system_token = models.TextField(
        verbose_name="ключ (токен) внешней системы",
        unique=True,
    )
    name = models.TextField(verbose_name="наименование")
    description = TextField(verbose_name="описание")
    url = models.TextField(verbose_name="путь API внешней ИС")
    created = models.DateTimeField(verbose_name="создан", auto_now_add=True)
    permission = models.ManyToManyField(
        verbose_name="разрешения",
        to=Permission,
        related_name="external_system_token",
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ключи авторизации"
        verbose_name_plural = "ключи авторизации"
        permissions = [
            ("can_get_system_manuals", "Может получать справочники системы"),
            ("can_sinchronize_user", "Может синхронизировать пользователей внешней ИС с АГ"),
            ("can_get_encouragements", "Может получать список поощрений"),
            ("can_get_suggestions", "Может получать список предложений"),
            ("can_get_votes", "Может получать список голосований"),
            ("can_get_initiatives", "Может получать список инициатив"),
            ("can_transmit_encouragements", "Может передавать список поощрений"),
            ("can_transmit_suggestions", "Может передавать список предложений"),
            ("can_get_user_balance", "Может получать баланс пользователя"),
            ("can_transmit_bonuses", "Может передавать бонусы"),
            ("can_get_operation_history_of_user", "Может получать историю операций пользователя"),
            ("can_transmit_citizen_category", "Может передавать категории граждан"),
            ("can_use_suggestions", "Может использовать бонусную систему в части предложений"),
            ("can_use_encouragements", "Может использовать бонусную систему в части поощрений"),
        ]
