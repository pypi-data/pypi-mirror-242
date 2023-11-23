from django.db.models.signals import post_save
from django.dispatch import receiver

from modules.core.models import ActiveCitizenModule
from modules.core.models.active_citizen_module import ActiveCitizenModuleEnum


@receiver(post_save, sender=ActiveCitizenModule)
def update_ecology_module_status(sender, instance, **kwargs):
    if instance.name in [ActiveCitizenModuleEnum.ECOLOGY_STIMULATION, ActiveCitizenModuleEnum.ECOLOGY_OFFERS]:
        has_stimulation = ActiveCitizenModule.objects.filter(
            name=ActiveCitizenModuleEnum.ECOLOGY_STIMULATION,
            is_worked=True
        ).exists()

        has_offers = ActiveCitizenModule.objects.filter(
            name=ActiveCitizenModuleEnum.ECOLOGY_OFFERS,
            is_worked=True
        ).exists()
        ecology_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.ECOLOGY).first()
        if not has_stimulation and not has_offers:
            if ecology_module:
                ecology_module.is_worked = False
                ecology_module.save()
        else:
            if ecology_module:
                ecology_module.is_worked = True
                ecology_module.save()