from rest_framework import serializers

from modules.appeals.models import Category


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
            "color",
            "image",
            "icon",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        ref_name = 'appeals_category_serializer'


class CategoryDetailedSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "color",
            "image",
            "icon",
            "parent",
        ]
        ref_name = 'appeals_category_detailed_serializer'

    def get_parent(self, instance):
        return (
            CategoryDetailedSerializer(instance.parent).data
            if instance.parent
            else None
        )


class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "color",
            "image",
            "icon",
            "children",
        ]

    def get_children(self, instance):
        return CategoryTreeSerializer(instance.children, many=True).data
