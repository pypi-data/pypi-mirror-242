from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from modules.core.models import User
from modules.ecology.api.serializers import GoodsNServicesItemFullDetailsSerializer
from modules.ecology.models import UserPurchase


class UserPurchaseSerializer(serializers.ModelSerializer):
    goods_n_services_item = GoodsNServicesItemFullDetailsSerializer()

    class Meta:
        model = UserPurchase
        fields = [
            "id",
            "status",
            "code",
            "timestamp",
            "goods_n_services_item",
        ]


class PartnerPurchaseSerializer(serializers.ModelSerializer):
    reward_id = serializers.IntegerField(source="goods_n_services_item.id")
    reward_name = serializers.CharField(source="goods_n_services_item.name")
    reward_cost = serializers.IntegerField(source="goods_n_services_item.cost")
    locality = serializers.CharField(source="goods_n_services_item.locality")
    user_FIO = serializers.SerializerMethodField(method_name="get_user_FIO")

    class Meta:
        model = UserPurchase
        fields = (
            "id",
            "reward_id",
            "reward_name",
            "reward_cost",
            "locality",
            "timestamp",
            "user_FIO",
        )

    def get_user_FIO(self, instance):
        user: User = instance.user
        if not user:
            raise ValidationError("Участник не передан")
        return f"{user.last_name} {user.first_name} {user.patronymic_name}"
