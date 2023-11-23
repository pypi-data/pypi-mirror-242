from django.core.exceptions import MultipleObjectsReturned
from rest_framework import serializers

from modules.core.models import User, CategoryCitizen
from modules.ecology.models import Notification, UserBalanceOperation, UserState
from modules.ecology.models import UserProfile as EcologyUserProfile


class NotificationSerializer(serializers.ModelSerializer):
    operation_type = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    message = serializers.CharField(source="text")
    date = serializers.DateTimeField(source="timestamp")

    class Meta:
        model = Notification
        fields = [
            "id",
            "operation_type",
            "amount",
            "message",
            "date",
        ]

    @staticmethod
    def get_operation_type(obj):
        return obj.user_balance_operation.type if obj.user_balance_operation else None

    @staticmethod
    def get_amount(obj):
        return obj.user_balance_operation.amount if obj.user_balance_operation else None


class NotificationCreateSerializer(serializers.ModelSerializer):
    operation_type = serializers.CharField(source="type")
    amount = serializers.IntegerField()
    message = serializers.CharField(source="text")
    date = serializers.DateTimeField(source="timestamp")

    class Meta:
        model = Notification
        fields = [
            "id",
            "operation_type",
            "amount",
            "message",
            "date",
        ]


class UserSerializer(serializers.ModelSerializer):
    locality = serializers.IntegerField(source="registration_locality_id")
    name = serializers.CharField(source="first_name")
    surname = serializers.CharField(source="last_name")
    patronymic = serializers.CharField(source="patronymic_name")
    is_active = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    operations = NotificationSerializer(many=True, source="notifications")
    balance = serializers.IntegerField(source="ecology.balance")
    bonus_active = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "locality",
            "name",
            "surname",
            "patronymic",
            "phone",
            "snils",
            "esia_verified",
            "bonus_active",
            "is_active",
            "balance",
            "categories",
            "operations",
            "last_login",
            "date_joined",
        ]

    @staticmethod
    def get_bonus_active(obj):
        if hasattr(obj, "ecology_profile"):
            return obj.ecology_profile.state != UserState.INITIAL
        return False

    @staticmethod
    def get_is_active(obj):
        return not obj.is_archive

    @staticmethod
    def get_categories(obj):
        return [cat.name for cat in obj.categories.all()]


class UserECardGetSerializer(UserSerializer):
    @staticmethod
    def get_is_active(obj):
        return obj.is_active


class UserUpdateSerializer(serializers.ModelSerializer):
    locality = serializers.IntegerField(source="registration_locality_id")
    name = serializers.CharField(source="first_name")
    surname = serializers.CharField(
        source="last_name",
        required=False,
        allow_null=True,
    )
    patronymic = serializers.CharField(
        source="patronymic_name",
        required=False,
        allow_null=True,
    )
    is_active = serializers.BooleanField(
        required=False,
        allow_null=True,
    )
    categories = serializers.ListSerializer(
        child=serializers.CharField(),
        required=False,
        allow_null=True,
    )
    operations = NotificationCreateSerializer(
        many=True,
        source="notifications",
        required=False,
        allow_null=True,
    )
    balance = serializers.IntegerField(
        source="ecology.balance",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "locality",
            "name",
            "surname",
            "patronymic",
            "is_active",
            "balance",
            "categories",
            "operations",
        ]

    def update(self, instance, validated_data):
        notifications = validated_data.pop("notifications", [])
        categories = validated_data.pop("categories", [])
        validated_data["is_archive"] = not validated_data.pop("is_active", False)

        for notification in notifications:
            timestamp = notification.pop("timestamp")
            try:
                operation, _ = UserBalanceOperation.objects.update_or_create(
                    user=instance,
                    type=notification.pop("type"),
                    amount=notification.pop("amount"),
                    timestamp=timestamp,
                )

                if not operation.notifications.exists():
                    Notification.objects.create(
                        **notification,
                        timestamp=timestamp,
                        user=instance,
                        user_balance_operation=operation
                    )
            except MultipleObjectsReturned:
                pass
        created_category = []
        for name in categories:
            try:
                category, _ = CategoryCitizen.objects.update_or_create(
                    name=name,
                )
                created_category.append(category.id)
            except MultipleObjectsReturned:
                pass
        if "ecology" in validated_data:
            ecology, _ = EcologyUserProfile.objects.get_or_create(user=instance)
            ecology.balance = validated_data.pop("ecology")["balance"]
            ecology.save()
        update: User = super().update(instance, validated_data)
        for i in created_category:
            update.categories.add(i)

        return update

    def to_representation(self, instance):
        return UserSerializer(instance).data
