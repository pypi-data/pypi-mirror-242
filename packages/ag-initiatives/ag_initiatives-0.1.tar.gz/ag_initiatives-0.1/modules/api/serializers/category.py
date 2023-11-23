import random

from rest_framework import serializers

from modules.api.serializers import FileShortSerializer
from modules.core.models import Category


class CategorySerializer(serializers.ModelSerializer):
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
        ref_name = 'api_category_serializer'

    def get_image(self, category: Category):
        try:
            return serializers.FileField().to_representation(
                random.choice(list(category.images.all())).file
            )
        except IndexError:
            return None


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "color",
        ]
