from rest_framework import serializers

from config.settings import DOMAIN_NAME, MEDIA_URL
from modules.api.serializers.initiative_accepting_settings import InitiativeAcceptingSettingsSerializer
from modules.api.serializers.initiative_operator_communication import InitiativeOperatorCommunicationListSerializer
from modules.initiatives.models import Initiative, InitiativeCategory
from modules.integration.api.serializers.voting import LocalityVoteSerializer


class InitiativeCategoryParentSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = InitiativeCategory
        fields = [
            "id",
            "name",
            "color",
            "image",
            "parent",
        ]

    @staticmethod
    def get_parent(obj):
        return (
            InitiativeCategoryParentSerializer(obj.parent).data
            if obj.parent
            else None
        )

    @staticmethod
    def get_image(obj):
        return f"{DOMAIN_NAME}{MEDIA_URL}{obj.image}"


class InitiativeCategoryChildrenSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = InitiativeCategory
        fields = [
            "id",
            "name",
            "color",
            "image",
            "children",
        ]

    @staticmethod
    def get_children(instance):
        return InitiativeCategoryChildrenSerializer(instance.children, many=True).data


class InitiativeIntegrationSerializer(serializers.ModelSerializer):
    category = InitiativeCategoryParentSerializer()
    locality = LocalityVoteSerializer(many=True)
    settings = InitiativeAcceptingSettingsSerializer()
    initiative_operator_communication = InitiativeOperatorCommunicationListSerializer(many=True)
    user_has_initiative = serializers.BooleanField(required=False)
    user_created_initiative = serializers.BooleanField(required=False)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Initiative
        fields = [
            "id",
            "url",
            "number",
            "user",
            "email",
            "settings",
            "date_of_report_publication",
            "date_of_decision",
            "title",
            "votes_threshold",
            "duration_month",
            "votes_threshold",
            "description",
            "expectations",
            "files",
            "state",
            "moderation_begin_date",
            "votes_collection_begin_date",
            "date_of_report_publication",
            "date_of_decision",
            "pdf_export",
            "category",
            "locality",
            "initiative_operator_communication",
            "user_has_initiative",
            "user_created_initiative",
        ]

    @staticmethod
    def get_url(obj):
        return f"{DOMAIN_NAME}/initiatives/details/{obj.id}"

    def get_is_voted(self, instance: Initiative):
        request = self.context.get("request", None)

        if request is None:
            return False

        return instance.is_voted(request.user)
