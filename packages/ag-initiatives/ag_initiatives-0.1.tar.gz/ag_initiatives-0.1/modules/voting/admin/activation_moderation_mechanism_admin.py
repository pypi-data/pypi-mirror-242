from django.contrib import admin

from ..models.activation_moderation_mechanism import ActivationModerationMechanism


class ActivationModerationMechanismAdmin(admin.ModelAdmin):
    list_display = ["active", "date_operation"]

admin.site.register(ActivationModerationMechanism, ActivationModerationMechanismAdmin)
