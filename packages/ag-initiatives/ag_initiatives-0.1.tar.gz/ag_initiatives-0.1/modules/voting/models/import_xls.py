from django.db import models

from modules.core.models import User


class ImportXlsModelManager(models.Manager):
    def get_queryset(self):
        return User.objects.none()


class ImportXlsModel(models.Model):
    objects = ImportXlsModelManager()

    file = models.FileField()

    def save(self, *args, **kwargs):
        from modules.core.services import import_xls

        import_xls(self.file.read())

    class Meta:
        managed = False
        verbose_name = "Импорт голосований"
        verbose_name_plural = "Импорт голосований"
