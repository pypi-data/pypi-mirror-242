import uuid

from django.db import models

from modules.core.models import DepartmentStatus


class LocalVotingGroup(models.Model):
    """Модель: Группа участников локального голосования"""

    class Meta:
        ordering = [
            "department",
            "name",
        ]
        indexes = [models.Index(fields=["name"])]
        verbose_name = "Группа участников локального голосования"
        verbose_name_plural = "Группы участников локального голосования"

    access_token = models.UUIDField(
        verbose_name="Токен доступа к голосованию",
        unique=True,
        default=uuid.uuid4,
        auto_created=True,
        editable=False,
    )

    name = models.CharField(
        verbose_name="Название", max_length=1000, null=False, blank=False
    )
    department = models.ForeignKey(
        verbose_name="Министерство",
        to="core.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )

    @property
    def participants_count(self):
        return self.participants.count()

    # @property
    # def participant_list(self):
    #     x = self.participants.all().values_list("email")
    #     y = []
    #     for it in x:
    #         y.append(*it)
    #     return y

    participants_count.fget.short_description = "Количество участников"

    def __str__(self):
        return f"{self.name} ({self.department}): количество участников - {self.participants_count}"
