import collections

from django.core.validators import FileExtensionValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class FileType:
    IMAGE = "IMAGE"
    DOCUMENT = "DOCUMENT"

    RESOLVER = collections.OrderedDict(
        [
            (IMAGE, "Изображение"),
            (DOCUMENT, "Документ"),
        ]
    )

    CHOICES = RESOLVER.items()


def validate_file_size(file):
    if file.size > 10485760:
        raise ValidationError("Файл слишком большой")


class File(models.Model):
    file = models.FileField(
        verbose_name="Файл",
        upload_to="appeals_pos",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "txt",
                    "doc",
                    "docx",
                    "rtf",
                    "xls",
                    "xlsx",
                    "pps",
                    "ppt",
                    "pptx",
                    "odt",
                    "ods",
                    "pub",
                    "pdf",
                    "jpg",
                    "jpeg",
                    "bpm",
                    "png",
                    "tif",
                    "gif",
                    "pcx",
                    "mp3",
                    "wma",
                    "avi",
                    "mp4",
                    "mkv",
                    "wmv",
                    "wma",
                    "mov",
                    "flv",
                ]
            ),
            validate_file_size,
        ],
    )
    smev_adapter_id = models.UUIDField(null=True, blank=True, verbose_name="Идентификатор ПОС")
    pos_id = models.UUIDField(null=True, blank=True, verbose_name="Идентификатор ПОС")
    send_to_pos = models.BooleanField(
        verbose_name='Файл направлен в ПОС',
        default=False,
    )
    type = models.TextField(
        choices=FileType.CHOICES, verbose_name="Тип файла", default=FileType.DOCUMENT
    )
    name = models.TextField(
        verbose_name="Имя файла",
    )
    owner = models.ForeignKey(
        to="core.User",
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        related_name="appeals_files",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
