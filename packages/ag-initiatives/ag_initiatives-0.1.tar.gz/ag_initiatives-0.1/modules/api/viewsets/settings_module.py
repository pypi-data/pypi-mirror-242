from rest_framework import viewsets

from modules.api.filters import SettingsTypeFilter
from modules.api.serializers import SettingsModuleSerializer
from modules.core.models import SettingsModule


class SettingsModuleAPI(viewsets.ReadOnlyModelViewSet):
    """ API для модели настройки (модулей)."""
    queryset = SettingsModule.objects.all()
    serializer_class = SettingsModuleSerializer
    filterset_class = SettingsTypeFilter
