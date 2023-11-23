from rest_framework import serializers

from modules.subscriptions.models import SubscriptionTemplate


class SubscriptionTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionTemplate
        fields = "__all__"
