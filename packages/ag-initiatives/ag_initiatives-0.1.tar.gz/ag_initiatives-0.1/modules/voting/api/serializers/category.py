import random

from rest_framework import serializers

from modules.api.serializers import FileShortSerializer
from modules.core.models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "color",
        ]


class CategoryDetailsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_files = FileShortSerializer(source="images", many=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "color",
            "image",
            "image_files",
        ]

    def get_image(self, category: Category):
        try:
            return serializers.FileField().to_representation(
                random.choice(list(category.images.all())).file
            )
        except IndexError:
            return None
