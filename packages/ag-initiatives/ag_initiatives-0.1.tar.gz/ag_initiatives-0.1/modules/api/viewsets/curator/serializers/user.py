from rest_framework import serializers

from modules.api.viewsets.admin_lko.serializers.user import AdminLkoUserShortSerializer, AdminLkoUserDetailSerializer


class CuratorUserShortSerializer(AdminLkoUserShortSerializer):
    pass


class CuratorUserDetailSerializer(AdminLkoUserDetailSerializer):
    pass
