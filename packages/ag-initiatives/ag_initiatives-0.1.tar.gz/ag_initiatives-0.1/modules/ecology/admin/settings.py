from django.contrib import admin
from django.utils.translation import gettext as _

from modules.ecology.models import Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ["description"]

    fieldsets = (
        [
            _("Награды"),
            {
                "fields": [
                    "participation_reward",
                    "survey_reward",
                    "add_initiative_reward",
                    "approve_initiative_reward",
                    "vote_reward",
                ]
            },
        ],
        [
            _("Текстовые константы"),
            {"fields": ["status_instruction", "module_information"]},
        ],
        [
            _("Экологический статус"),
            {
                "fields": [
                    ("min_beginner_bonuses", "max_beginner_bonuses"),
                    ("min_dweller_bonuses", "max_dweller_bonuses"),
                    ("min_city_expert_bonuses", "max_city_expert_bonuses"),
                    "min_active_citizen_bonuses",
                ],
            },
        ],
    )

    def description(self, obj):
        return "Нажмите, чтобы внести изменения в настройки"

    description.short_description = "Настройки"
