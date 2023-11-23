from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from modules.voting.models import ActivationModerationMechanism

class ActivationModerationMechanismSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivationModerationMechanism
        fields = "__all__"