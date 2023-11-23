from rest_framework import serializers

from modules.core.models import LkoVotingDescription


class LkoVotingDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LkoVotingDescription
        fields = ["description_id", "text", "voting_type"]
