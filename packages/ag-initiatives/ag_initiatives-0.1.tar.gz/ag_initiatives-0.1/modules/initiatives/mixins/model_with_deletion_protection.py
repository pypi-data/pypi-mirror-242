from django.db import models


class QuerySetWithoutDeleted(models.query.QuerySet):
    def delete(self):
        for obj in self:
            ModelWithDeletionProtection.delete(obj)


class NoDeleteManager(models.Manager):
    def get_queryset(self):
        return QuerySetWithoutDeleted(self.model, using=self._db).filter(is_deleted=False)


class ModelWithDeletionProtection(models.Model):
    """
    Модель с защитой от удаления
    (скрывает удаленные объекты, но оставляет их в БД)
    """
    is_deleted = models.BooleanField(
        verbose_name="Удалён",
        default=False,
        editable=False,
    )

    def delete(self, *args, **kwargs):
        from django.contrib.admin.utils import NestedObjects
        collector = NestedObjects(using="default")
        collector.collect([self])
        # Проверка на отсутствие связных объектов
        if len(collector.data) <= 1:
            return super().delete(*args, **kwargs)
        self.is_deleted = True
        return super().save(*args, **kwargs)

    objects = NoDeleteManager()

    class Meta:
        abstract = True
