from rest_framework import serializers

from modules.core.models import User, CategoryCitizen


class UserCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("categories",)

    def update(self, instance, validated_data):
        instance.categories.clear()
        categories = validated_data["categories"]
        for category in categories:
            instance.categories.add(category)
        instance.save()


class CategoryCitizenSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryCitizen
        fields = ("id", "name")
