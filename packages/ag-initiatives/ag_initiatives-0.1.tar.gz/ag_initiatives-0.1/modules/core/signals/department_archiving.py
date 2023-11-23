from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver

from modules.core.models import DepartmentStatus, User, OperatorLkoPermissions, AdminLkoPermissions, Department


@receiver(pre_save, sender=Department)
def archive_users(sender, instance, **kwargs):
    try:
        department = Department.objects.get(id=instance.id)
        if instance.status == DepartmentStatus.ARCHIVED:
            users = User.objects.filter(
                Q(operator_permissions__department=department) |
                Q(admin_lko_permissions__department=department) |
                Q(sub_permissions__operator_permissions__department=department) |
                Q(sub_permissions__admin_lko_permissions__department=department)
            )
            for user in users:
                user.is_archive = True
                user.save()
    except ObjectDoesNotExist:
        pass


@receiver(pre_save, sender=Department)
def unarchive_users(sender, instance, **kwargs):
    try:
        department = Department.objects.get(id=instance.id)
        if instance.status != DepartmentStatus.ARCHIVED:
            users = User.objects.filter(
                (Q(operator_permissions__department=department) |
                 Q(admin_lko_permissions__department=department) |
                 Q(sub_permissions__operator_permissions__department=department) |
                 Q(sub_permissions__admin_lko_permissions__department=department)
                 ))
            for user in users:
                user.is_archive = False
                user.save()
    except ObjectDoesNotExist:
        pass
