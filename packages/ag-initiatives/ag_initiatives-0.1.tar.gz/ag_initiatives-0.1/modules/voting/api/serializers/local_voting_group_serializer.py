from typing import List

from django.db.models import Q
from rest_framework import serializers

from modules.api.serializers import DepartmentShortSerializer
from modules.core.models import Department
from modules.voting.api.serializers import VotingParticipantSerializer, VotingParticipantCreateSerializer
from modules.voting.models import LocalVotingGroup, VotingParticipant


class VotingParticipantListingField(serializers.RelatedField):

    def to_representation(self, value):
        return VotingParticipantSerializer(value).data

    def to_internal_value(self, data):
        model = self.queryset.model
        if str(data).isdigit():
            obj = model.objects.get_or_create(pk=data)[0]
        else:
            obj = model.objects.get_or_create(**data)[0]
        return obj


class DepartmentField(serializers.RelatedField):
    # queryset = Department.objects.all()

    def to_representation(self, value):
        return {"id": value.id, "name": value.name}

    def to_internal_value(self, data):
        if str(data).isdigit():
            obj = self.queryset.filter(pk=data).first()
        else:
            obj = self.queryset.filter(pk=data.get("id", 0)).first()
        return obj


class LocalVotingGroupSerializer(serializers.ModelSerializer):

    access_token = serializers.UUIDField(read_only=True)
    participants = VotingParticipantSerializer(many=True)
    department = DepartmentShortSerializer()

    class Meta:
        model = LocalVotingGroup
        fields = "__all__"


class LocalVotingGroupCreateSerializer(serializers.ModelSerializer):

    participants = VotingParticipantCreateSerializer(many=True)

    class Meta:
        model = LocalVotingGroup
        exclude = ["access_token"]

    def create(self, validated_data):
        participants_data = validated_data.pop("participants")
        group = LocalVotingGroup.objects.create(**validated_data)

        participants: List[VotingParticipant] = []

        for participant_data in participants_data:
            participant_data["group"] = group.id
            participant_serializer = VotingParticipantCreateSerializer(data=participant_data)
            participant_serializer.is_valid(raise_exception=True)
            participant = participant_serializer.save()
            participants.append(participant)

        VotingParticipant.objects.bulk_create(participants)
        return group

    def update(self, instance: LocalVotingGroup, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.department_id = validated_data.get("department", instance.department_id)
        instance.save(update_fields=["department", "name"])

        participants_ids_with_nones = list(map(
            lambda data: data.get("id"), validated_data.get("participants")
        ))
        participants_ids = list(filter(
            lambda v: v is not None, participants_ids_with_nones
        ))

        instance.participants.filter(~Q(pk__in=participants_ids)).delete()

        participants_to_create: List[VotingParticipant] = []

        for participant_data in validated_data.get("participants"):

            if not participant_data.get("id", None):
                participant = VotingParticipant(**participant_data)
                participant.group = instance
                participants_to_create.append(participant)
            else:
                participant_instance = VotingParticipant.objects.get(pk=participant_data.get("id"))
                participant_serializer = VotingParticipantCreateSerializer(
                    instance=participant_instance, data=participant_data
                )
                participant_serializer.is_valid(raise_exception=True)
                participant_serializer.save()

        VotingParticipant.objects.bulk_create(participants_to_create)

        return instance
