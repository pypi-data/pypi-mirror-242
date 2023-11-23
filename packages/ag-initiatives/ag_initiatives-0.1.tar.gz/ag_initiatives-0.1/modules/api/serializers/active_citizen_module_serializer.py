from rest_framework import serializers

from modules.core.models import ActiveCitizenModule
from modules.core.models.active_citizen_module import ActiveCitizenModuleEnum


class ActiveCitizenModuleSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField()

    @classmethod
    def get_display_name(cls, obj):
        return ActiveCitizenModuleEnum.DISPLAY_RESOLVER.get(obj.display_name, None)

    class Meta:
        model = ActiveCitizenModule
        fields = "__all__"
