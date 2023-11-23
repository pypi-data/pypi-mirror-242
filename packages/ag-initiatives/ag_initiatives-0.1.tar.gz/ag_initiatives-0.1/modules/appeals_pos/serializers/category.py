from rest_framework import serializers

from modules.appeals_pos.models.category import Category
from modules.appeals_pos.models.subcategory import Subcategory


class CategoryFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "color",
            "image",
            "icon",
        ]


class CategoryTreeSerializer(serializers.ModelSerializer):

    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def get_subcategories(self, instance: Category):
        queryset = instance.subcategories
        return SubcategoryShortSerializer(queryset, many=True).data


class SubcategoryFullSerializer(serializers.ModelSerializer):

    category = CategoryFullSerializer()
    image = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = "__all__"

    def get_image(self, instance: Subcategory):
        return instance.category.image.url if instance.category.image else None

    def get_icon(self, instance: Subcategory):
        return instance.category.icon.url if instance.category.icon else None


class SubcategoryShortSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = ["id", "pos_id", "name", "image", "icon"]

    def get_image(self, instance: Subcategory):
        return instance.category.image.url if instance.category.image else None

    def get_icon(self, instance: Subcategory):
        return instance.category.icon.url if instance.category.icon else None
