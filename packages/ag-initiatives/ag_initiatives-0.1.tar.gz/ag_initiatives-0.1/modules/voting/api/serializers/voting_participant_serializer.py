from rest_framework import serializers

from modules.voting.models import VotingParticipant


class VotingParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingParticipant
        exclude = ["group"]


class VotingParticipantCreateSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = VotingParticipant
        fields = "__all__"

    def create(self, validated_data):
        return VotingParticipant(**validated_data)

    def update(self, instance: VotingParticipant, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.patronymic_name = validated_data.get("patronymic_name", instance.patronymic_name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
        return instance

