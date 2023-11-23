from django.db.models import Q
from rest_framework import serializers

from modules.initiatives.models import (
    Initiative,
    InitiativeOperatorCommunicationType,
    InitiativeOperatorCommunication,
)
from modules.initiatives.models.initiative_operator_communication import (
    ModerateResponseState,
)


class InitiativeOperatorCommunicationPDFSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(format="%H:%M:%S %d:%m:%Y")
    type = serializers.SerializerMethodField()

    class Meta:
        model = InitiativeOperatorCommunication
        fields = ("username", "timestamp", "type", "text")

    def get_username(self, instance):
        fn = instance.user.first_name if instance.user else ""
        ln = instance.user.patronymic_name if instance.user else ""
        pn_s = instance.user.last_name if instance.user else ""
        return f"{fn} {ln} {pn_s}."

    def get_type(self, instance):
        return InitiativeOperatorCommunicationType.RESOLVER.get(instance.type)


class InitiativePDFSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_email = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    parent_category = serializers.SerializerMethodField()
    communications = InitiativeOperatorCommunicationPDFSerializer(many=True)
    locality = serializers.SerializerMethodField()
    creation_date_time = serializers.DateTimeField(format="%H:%M:%S %d:%m:%Y")

    class Meta:
        model = Initiative
        fields = (
            "creation_date_time",
            "number",
            "locality",
            "author_name",
            "author_email",
            "category",
            "parent_category",
            "title",
            "description",
            "expectations",
            "communications",
        )

    def get_author_name(self, instance: Initiative):
        fn = instance.user.first_name or ""
        ln = instance.user.patronymic_name or ""
        pn_s = instance.user.last_name if instance.user.last_name else ""
        return f"{fn} {ln} {pn_s}."

    def get_author_email(self, instance: Initiative):
        return instance.email

    def get_locality(self, instance: Initiative):
        return instance.locality.name

    def get_category(self, instance: Initiative):
        return instance.category.name

    def get_parent_category(self, instance: Initiative):
        parent = instance.category.parent
        if parent:
            return parent.name
        return ""

    def get_communications(self, instance: Initiative):
        qs = instance.communications.filter(
            Q(type=InitiativeOperatorCommunicationType.MODERATE_REQUEST)
            | (
                Q(state=ModerateResponseState.APPROVED)
                & Q(type=InitiativeOperatorCommunicationType.MODERATE_RESPONSE)
            )
        )
        return InitiativeOperatorCommunicationPDFSerializer(list(qs), many=True).data
