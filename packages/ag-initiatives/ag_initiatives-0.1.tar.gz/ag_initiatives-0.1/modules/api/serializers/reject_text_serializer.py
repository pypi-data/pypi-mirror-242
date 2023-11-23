from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from modules.initiatives.models import (
    InitiativeOperatorCommunication,
    InitiativeOperatorCommunicationType,
)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from modules.initiatives.models import InitiativeRejectReason
from modules.initiatives.models.initiative_operator_communication import (
    ModerateResponseState,
)


class CommunicationFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeOperatorCommunication
        fields = ("files",)


class CommunicationTextFilesSerializer(CommunicationFilesSerializer):
    text = serializers.CharField(required=True)

    class Meta:
        model = CommunicationFilesSerializer.Meta.model
        fields = CommunicationFilesSerializer.Meta.fields + ("text",)


class CommunicationReasonFilesSerializer(CommunicationFilesSerializer):
    reason = serializers.IntegerField()

    class Meta:
        model = CommunicationFilesSerializer.Meta.model
        fields = CommunicationFilesSerializer.Meta.fields + ("reason",)

    def validate_reason(self, value):
        reason = InitiativeRejectReason.objects.filter(pk=value).first()
        if reason:
            return reason.text
        raise ValidationError(code=400)

    def to_internal_value(self, data):
        data = super(CommunicationFilesSerializer, self).to_internal_value(data)
        data["text"] = data.pop("reason")
        return data


class MessagingMixin:
    def perform_create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["timestamp"] = timezone.now()
        files = None
        if "files" in validated_data:
            files = validated_data.pop("files")
        message = InitiativeOperatorCommunication.objects.create(**validated_data)
        if files:
            message.files.set(files)
        return message


class MessagingResponseSerializer(MessagingMixin, CommunicationTextFilesSerializer):
    answer_to = serializers.IntegerField()

    class Meta:
        model = CommunicationTextFilesSerializer.Meta.model
        fields = CommunicationTextFilesSerializer.Meta.fields + ("answer_to",)

    def validate_answer_to(self, value):
        communication = InitiativeOperatorCommunication.objects.filter(
            Q(id=value)
            & Q(
                type__in=(
                    InitiativeOperatorCommunicationType.MODERATE_REQUEST,
                    InitiativeOperatorCommunicationType.PREMODERATE_REQUEST,
                )
            )
            & Q(user_viewed=False)
        ).first()
        if communication:
            return communication
        raise ValidationError("Недопустимый ответ.")

    def create(self, validated_data):
        initiative = self.context["initiative"]
        validated_data["initiative"] = initiative
        communication_to_answer = validated_data.pop("answer_to")
        if (
            communication_to_answer.type
            == InitiativeOperatorCommunicationType.MODERATE_REQUEST
        ):
            validated_data["state"] = ModerateResponseState.MODERATION_REQUIRED
            validated_data[
                "type"
            ] = InitiativeOperatorCommunicationType.MODERATE_RESPONSE
        else:
            validated_data[
                "type"
            ] = InitiativeOperatorCommunicationType.PREMODERATE_RESPONSE
        validated_data["user_viewed"] = True
        communication_to_answer.user_viewed = True
        communication_to_answer.save()
        self.perform_create(validated_data)


class MessagingRequestSerializer(MessagingMixin, CommunicationTextFilesSerializer):
    class Meta:
        model = CommunicationTextFilesSerializer.Meta.model
        fields = CommunicationTextFilesSerializer.Meta.fields

    def create(self, validated_data):
        user = self.context["request"].user
        initiative = self.context["initiative"]
        validated_data["initiative"] = initiative
        if user.is_moderator:
            validated_data[
                "type"
            ] = InitiativeOperatorCommunicationType.PREMODERATE_REQUEST
            validated_data["moderator_viewed"] = True
        elif user.is_operator:
            validated_data[
                "type"
            ] = InitiativeOperatorCommunicationType.MODERATE_REQUEST
            validated_data["operator_viewed"] = True
        else:
            raise ValidationError(code=400)
        self.perform_create(validated_data)
