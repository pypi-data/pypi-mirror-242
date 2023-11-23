from adminsortable.models import SortableMixin
from django.db import models

class BlockFile(models.Model):
    name = models.CharField(
        verbose_name='Наименование файла',
        max_length=100,
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to="import/modules/%Y/%m/%d",
    )

    def __str__(self):
        if self.file.name:
            return f'{self.name} [{self.file.name.split("/")[-1]}]'
        else:
            return f'{self.name}'

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы из модулей'


class BlockLink(models.Model):
    name = models.CharField(
        verbose_name='Заголовок ссылки',
        max_length=100,
    )
    link = models.URLField(
        verbose_name='Ссылка',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки из модулей'


class ProjectInfo(SortableMixin):
    project_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    block_id = models.TextField(
        verbose_name="Описание",
        blank=True,
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    video = models.ForeignKey(
        to="core.Video",
        on_delete=models.CASCADE,
        verbose_name="Видео",
        default=None,
        null=True,
        blank=True,
    )
    image = models.ForeignKey(
        to="core.Image",
        on_delete=models.SET_NULL,
        verbose_name="Изображение",
        default=None,
        null=True,
        blank=True,
    )
    site_module = models.ForeignKey(
        to='core.ActiveCitizenModule',
        verbose_name='Блок страницы',
        blank=True, null=True,
        editable=False,
        related_name='blocks',
        on_delete=models.CASCADE,
    )
    is_project_info = models.BooleanField(
        default=True,
        editable=False,
        verbose_name='Блок раздела "О проекте"'
    )
    files_name = models.CharField(
        verbose_name='Описание файлов',
        max_length=100,
        blank=True, null=True,
    )
    files = models.ManyToManyField(
        to=BlockFile,
        verbose_name='Файлы',
        blank=True,
    )
    links = models.ManyToManyField(
        to=BlockLink,
        verbose_name='Ссылки',
        blank=True,
    )
    def __str__(self):
        return self.block_id

    class Meta:
        verbose_name = 'Блок'
        verbose_name_plural = 'Блоки'
        ordering = ['project_order']
