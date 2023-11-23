import django_filters

from modules.core.models import SettingsModule
from modules.core.models.settings_types import SettingsTypes


class SettingsTypeFilter(django_filters.FilterSet):
    """ Фильтр по типу настроек моделей."""
    settings_type = django_filters.ChoiceFilter(
        field_name='type',
        choices=[(item.name, item.value) for item in SettingsTypes],
    )

    class Meta:
        model = SettingsModule
        fields = ["type"]
