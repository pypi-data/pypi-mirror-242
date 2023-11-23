from django.contrib import admin

from config.settings import settings
from .category import InitiativeCategoryAdmin
from .initiative import InitiativeAdmin
from .initiative_accepting_settings import InitiativeAcceptingSettingsAdmin
from .initiative_reject_reason import InitiativeRejectReasonAdmin
from .initiative_settings import InitiativeSettingsAdmin
from .file import InitiativeFileAdmin


if settings.INVENTORY_STANDALONE:
    admin.site.unregister(category.InitiativeCategory)
    admin.site.unregister(initiative.Initiative)
    admin.site.unregister(initiative_accepting_settings.InitiativeAcceptingSettings)
    admin.site.unregister(initiative_reject_reason.InitiativeRejectReason)
    admin.site.unregister(initiative_settings.InitiativeSettings)
    admin.site.unregister(file.InitiativeFile)
