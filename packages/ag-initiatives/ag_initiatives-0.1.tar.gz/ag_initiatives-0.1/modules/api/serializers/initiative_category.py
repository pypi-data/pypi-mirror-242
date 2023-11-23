from rest_framework import serializers

from modules.initiatives.models import InitiativeCategory, InitiativeAcceptingSettings


class InitiativeCategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeCategory
        fields = [
            "id",
            "name",
            "color",
            "image",
        ]


class InitiativeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeCategory
        fields = "__all__"


class InitiativeCategoryDetailedSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = InitiativeCategory
        fields = [
            "id",
            "name",
            "color",
            "image",
            "parent",
        ]

    def get_parent(self, instance):
        return (
            InitiativeCategoryDetailedSerializer(instance.parent).data
            if instance.parent
            else None
        )


class InitiativeCategoryTreeSerializer(serializers.ModelSerializer):
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

    def get_children(self, instance):
        if recursion := instance.children.filter(id=instance.id):
            recursion[0].parent = None
            recursion[0].save()
        return InitiativeCategoryTreeSerializer(instance.children, many=True).data


class InitiativeCategoryAvailableSerializer(InitiativeCategoryTreeSerializer):
    class Meta:
        model = InitiativeCategoryTreeSerializer.Meta.model
        fields = InitiativeCategoryTreeSerializer.Meta.fields

    def get_children(self, instance):
        return InitiativeCategoryTreeSerializer(instance.children, many=True).data


class InitiativeAcceptingSettingsShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeAcceptingSettings
        fields = [
            "id",
            "department_name",
            "votes_threshold",
        ]


class InitiativeCategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeCategory
        fields = [
            "id",
            "name",
        ]
