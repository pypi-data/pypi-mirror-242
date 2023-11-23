from rest_framework import serializers

from modules.api.serializers import LocalityShortSerializer
from modules.core.services.locality import LocalityService
from modules.voting.api.serializers import VoteOperatorListSerializer
from modules.voting.models import Vote


class VoteOperatorLkoListSerializer(VoteOperatorListSerializer):
    locality_service = LocalityService()

    locality = serializers.SerializerMethodField()
    municipality = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = VoteOperatorListSerializer.Meta.fields + ["municipality"]

    def get_locality(self, vote: Vote):
        localities = self.locality_service.get_all_localities(vote.locality.all())
        return LocalityShortSerializer(localities, many=True).data

    def get_municipality(self, vote: Vote):
        municipalities = self.locality_service.get_all_localities(vote.locality.all())
        return LocalityShortSerializer(municipalities, many=True).data
