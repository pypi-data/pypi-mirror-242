from django.core.validators import FileExtensionValidator
from django.db import models

from modules.core.models import UserRole


class InstructionFile(models.Model):
    file = models.FileField(
        verbose_name="Файлы",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["doc", "docx", "pdf", "xlsx", "mp4", "mov", "mpeg4", "avi"]
            )
        ],
    )

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = "Инструкция по работе в системе"
        verbose_name_plural = "Инструкции по работе в системе"


class RoleInstruction(models.Model):
    role = models.TextField(
        choices=UserRole.CHOICES,
        verbose_name="Роль пользователя",
        unique=True,
    )
    instructions = models.ManyToManyField(
        to=InstructionFile,
        verbose_name="Инструкции",
        blank=True,
    )

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = "Назначение инструкций по ролям пользователей"
        verbose_name_plural = "Назначения инструкций по ролям пользователей"
