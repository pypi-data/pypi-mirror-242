from rest_framework import serializers

from modules.core.models import Department


class DepartmentShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "image",
            "email",
            "parent",
        ]


class DepartmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "image",
            "status",
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    parent = DepartmentShortSerializer(read_only=True)

    class Meta:
        model = Department
        fields = "__all__"


class DepartmentParentsTreeSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Department
        # fields = "__all__"
        fields = ["id", "name", "email", "status", "parent"]

    def get_parent(self, instance: Department):
        return DepartmentParentsTreeSerializer(instance.parent).data if instance.parent else None


class DepartmentTreeSerializer(serializers.ModelSerializer):
    sub_departments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "status", "sub_departments"]

    def get_sub_departments(self, instance: Department):
        return DepartmentTreeSerializer(instance.sub_departments, many=True).data


class DepartmentsMainTreeSerializer(serializers.ModelSerializer):
    sub_departments = serializers.SerializerMethodField(read_only=True)
    parent = DepartmentParentsTreeSerializer(read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "email", "status", "sub_departments", "parent"]

    def get_sub_departments(self, instance: Department):
        return DepartmentTreeSerializer(instance.sub_departments, many=True).data
