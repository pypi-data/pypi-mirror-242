from rest_framework import serializers

from modules.subscriptions.enums import EventEnum
from modules.subscriptions.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):

    event_display = serializers.SerializerMethodField(read_only=True)

    def get_event_display(self, instance):
        return instance.event_display

    module_display = serializers.SerializerMethodField(read_only=True)

    def get_module_display(self, instance):
        return instance.module_display

    category_display = serializers.SerializerMethodField(read_only=True)

    def get_category_display(self, instance):
        return instance.category_display

    class Meta:
        model = Subscription
        fields = "__all__"
