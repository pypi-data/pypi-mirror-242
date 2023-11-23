from typing import Union

from django.db import models

from .file import FileType
import os.path


class AppealAttachment(models.Model):
    appeal_answer = models.ForeignKey(
        to="appeals_pos.AppealAnswer",
        on_delete=models.CASCADE,
        verbose_name="Изменение состояния обращения",
        related_name="attachments",
    )
    pos_id = models.CharField(
        max_length=1000,
        verbose_name="Идентификатор файла ПОС",
    )
    file_name = models.CharField(
        max_length=1000,
        verbose_name="Имя файла",
        blank=True, null=True,
    )
    ftp_uuid = models.CharField(
        max_length=1000,
        verbose_name="UUID файла для FTP",
        blank=True, null=True,
    )
    ftp_username = models.CharField(
        max_length=1000,
        verbose_name="FTP логин",
        blank=True, null=True,
    )
    ftp_password = models.CharField(
        max_length=1000,
        verbose_name="FTP пароль",
        blank=True, null=True,
    )
    file = models.FileField(
        upload_to="appeals_pos",
        verbose_name="Файл",
        blank=True, null=True,
    )

    @property
    def type(self) -> Union[str, None]:
        if not self.file_name:
            return None
        extension = os.path.splitext(self.file_name)[1]
        return (FileType.IMAGE
                if extension in [
                    ".jpg",
                    ".jpeg",
                    ".bmp",
                    ".png",
                    ".tif",
                    ".gif",
                    ".pcx",
                ]
                else FileType.DOCUMENT)

    def __str__(self):
        return f'{self.file_name if self.file_name else "Файл ожидает загрузки"}'

    class Meta:
        verbose_name = "Файл из ПОС"
        verbose_name_plural = "Файлы из ПОС"
