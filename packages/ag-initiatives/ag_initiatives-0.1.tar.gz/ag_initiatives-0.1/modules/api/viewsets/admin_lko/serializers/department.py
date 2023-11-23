import logging
from abc import abstractmethod
from typing import Iterable

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from modules.api.serializers.category import CategoryShortSerializer as VotingCategorySerializer
from modules.api.serializers import InitiativeCategoryTreeSerializer, DepartmentShortSerializer
from modules.api.serializers.department import DepartmentTreeSerializer
from modules.core.models import Department, Locality, LocalityType, DepartmentSubPermissions, DepartmentSubInfo, \
    Municipality
from modules.core.models.permissions import ModulesPermissions
from modules.core.services import DepartmentService
from modules.core.services.department import DepartmentPermissionsServiceFactory, DepartmentListService
from modules.core.services.locality import LocalityService
from modules.feedback.api.v1.serializers import ProblematicSerializer
from modules.plans.api.serializers import CategoryShortSerializer as PlansCategorySerializer
from modules.map_works.api.serializers import WorkCategoryShortSerializer
from modules.appeals_pos.serializers import CategoryShortSerializer as AppealsCategorySerializer
from modules.ecology.api.serializers import GoodsNServicesItemCategoryShortSerializer as \
    EncouragementsCategorySerializer
from modules.ecology.api.serializers import EventCategoryShortSerializer as SuggestionsCategorySerializer

from modules.api.serializers.locality import MunicipalityWithUnavailableTreeSerializer, LocalitySerializer


class DepartmentSubPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentSubPermissions
        fields = [
            "modules_permissions",
            "voting_categories",
            "initiative_categories",
            "map_works_categories",
            "plans_categories",
            "appeals_categories",
            "suggestion_categories",
            "encouragement_categories",
        ]


class DepartmentSubInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentSubInfo
        exclude = ["department", "id"]

    def create(self, validated_data) -> DepartmentSubInfo:
        return DepartmentSubInfo.objects.create(**validated_data)

    def update(self, instance: DepartmentSubInfo, validated_data) -> DepartmentSubInfo:
        instance.short_name = validated_data.get("short_name", instance.short_name)
        instance.address = validated_data.get("address", instance.address)
        instance.ogrn = validated_data.get("ogrn", instance.ogrn)
        instance.inn = validated_data.get("inn", instance.inn)
        instance.kpp = validated_data.get("kpp", instance.kpp)
        instance.oktmo = validated_data.get("oktmo", instance.oktmo)
        instance.lko_type = validated_data.get("lko_type", instance.lko_type)
        instance.lko_level = validated_data.get("lko_level", instance.lko_level)
        instance.save(
            update_fields=[
                "short_name",
                "address",
                "ogrn",
                "inn",
                "kpp",
                "oktmo",
                "lko_type",
                "lko_level",
            ])
        return instance


class DepartmentsDetailSerializer(serializers.ModelSerializer):
    department_service = DepartmentListService()

    parent = DepartmentShortSerializer(read_only=True)
    sub_permissions = DepartmentSubPermissionsSerializer()
    sub_info = DepartmentSubInfoSerializer()

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "status",
            "email",
            "email_initiative_notification",
            "sub_departments",
            "parent",
            "locality",
            "image",
            "sub_permissions",
            "sub_info",
        ]


class DepartmentCreateSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    locality = serializers.ListSerializer(child=serializers.IntegerField(), required=False)
    sub_info = DepartmentSubInfoSerializer(required=False)
    is_new_image = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = Department
        fields = [
            "parent_id",
            "status",
            "email_initiative_notification",
            "name",
            "locality",
            "email",
            "sub_info",
            "is_new_image",
        ]

    def create(self, validated_data):

        try:
            parent = None
            if parent_id := validated_data.pop("parent_id", None):
                parent = Department.objects.get(pk=parent_id)
        except Department.DoesNotExist:
            raise ValidationError("Указана несуществующая подведомственная организация")

        validated_data.pop("is_new_image")

        localities = Locality.objects.filter(pk__in=validated_data.pop("locality", []))

        sub_info_data = validated_data.pop("sub_info", None)

        department = Department.objects.create(
            parent=parent,
            image=self.context.get("image"),
            # sub_departments=children,
            # locality=localities,
            **validated_data
        )
        department.locality.set(localities)

        if sub_info_data:
            DepartmentSubInfo.objects.create(department=department, **sub_info_data)

        return department

    def update(self, instance: Department, validated_data):
        try:
            parent = None
            if parent_id := validated_data.pop("parent_id", None):
                parent = Department.objects.get(pk=parent_id)
        except Department.DoesNotExist:
            raise ValidationError("Указана несуществующая подведомственная организация")

        localities = Locality.objects.filter(pk__in=validated_data.pop("locality", []))

        instance.parent = parent
        instance.locality.set(localities)
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        status = validated_data.get('status')
        if instance.status != status:
            DepartmentService.update_status_of_sub_departments(status, instance)
            if status == 'ARCHIVED':
                DepartmentService.update_status_of_sub_permissions_in_sub_departments(status=False, instance=instance)
            elif status == 'IS_ACTIVE':
                DepartmentService.update_status_of_sub_permissions_in_sub_departments(status=True, instance=instance)
        instance.status = validated_data.get("status", instance.status)
        instance.email_initiative_notification = validated_data.get("email_initiative_notification",
                                                                    instance.email_initiative_notification)

        instance.image = self.context.get("image") if validated_data.get("is_new_image") else instance.image
        instance.save()

        sub_info_data = validated_data.get("sub_info", None)

        if not sub_info_data:
            return instance

        if hasattr(instance, "sub_info"):
            sub_info_data['lko_level'] = sub_info_data['lko_level'].id if sub_info_data['lko_level'] is not None else None
            sub_info_data['lko_type'] = sub_info_data['lko_type'].id if sub_info_data['lko_type'] is not None else None
            serializer = DepartmentSubInfoSerializer(instance=instance.sub_info, data=sub_info_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            DepartmentSubInfo.objects.update_or_create(department=instance, **sub_info_data)

        return instance


class IDepartmentAllowedModuleSerializer(serializers.Serializer):
    allowed_categories = serializers.SerializerMethodField()
    allowed_municipalities = serializers.SerializerMethodField()
    department_service_factory = DepartmentPermissionsServiceFactory()

    @abstractmethod
    def get_allowed_categories(self, instance: Department):
        pass

    @abstractmethod
    def get_allowed_municipalities(self, instance: Department):
        pass

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


def get_divided_municipalities_data(municipalities: Iterable[Locality]) -> dict:
    municipal_regions = list(filter(
        lambda municipality: municipality.type.name == "Муниципальный район", municipalities
    ))
    municipal_districts = list(filter(
        lambda municipality: municipality.type.name == "Муниципальный округ", municipalities
    ))
    urban_districts = list(filter(
        lambda municipality: municipality.type.name == "Городской округ", municipalities
    ))

    return {
        "municipal_regions": MunicipalityWithUnavailableTreeSerializer(municipal_regions, many=True).data,
        "municipal_districts": MunicipalityWithUnavailableTreeSerializer(municipal_districts, many=True).data,
        "urban_districts": MunicipalityWithUnavailableTreeSerializer(urban_districts, many=True).data
    }


def get_municipalities_with_unavailable_from_localities(
        municipalities_with_localities: Iterable[Locality]
) -> Iterable[Locality]:
    """
    1. Фильтрует МО из общего списка МО и населенных пунктов
    2. Фильтрует населенные пункты, которые не являются детьми этих МО
    3. Достает MO из населенных пунктов во 2 пункте, метит их как недоступные, присваивает ему только доступных детей
        (они будут недоступны для редактирования, создания каких либо объектов)
    4. Объединяет их вместе

    Далее это все должно улетать в сериализатор, который знает о метках доступных, недоступных МО,
        а не просто строит дерево из всех существующих детей
    """
    locality_service = LocalityService()
    municipalities = list(locality_service.filter_municipalities(municipalities_with_localities))

    localities = locality_service.filter_localities(municipalities_with_localities)

    localities_from_municipalities = list(locality_service.filter_localities(
        locality_service.get_all_localities(municipalities)
    ))
    localities_without_municipalities = list(
        filter(lambda locality: locality not in localities_from_municipalities, localities)
    )

    unavailable_municipalities = []
    for locality in localities_without_municipalities:
        municipality = locality.parent

        if municipality is not None:

            if not hasattr(municipality, "is_available"):
                municipality.is_available = False

            if municipality not in unavailable_municipalities:
                unavailable_municipalities.append(municipality)

            for local_municipality in unavailable_municipalities:
                if municipality == local_municipality:
                    if not hasattr(local_municipality, "allowed_localities"):
                        local_municipality.allowed_localities = []

                    local_municipality.allowed_localities.append(locality)
                    break

    return municipalities + unavailable_municipalities


class DepartmentAllowedVotingInfoSerializer(IDepartmentAllowedModuleSerializer):

    def get_allowed_categories(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.VOTING, department=instance)
        return VotingCategorySerializer(service.get_allowed_categories(), many=True).data

    def get_allowed_municipalities(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.VOTING, department=instance)
        return get_divided_municipalities_data(service.get_allowed_municipalities())


class DepartmentAllowedInitiativeInfoSerializer(IDepartmentAllowedModuleSerializer):

    def get_allowed_categories(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.INITIATIVES, department=instance)
        return service.get_allowed_categories()

    def get_allowed_municipalities(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.INITIATIVES, department=instance)
        return get_divided_municipalities_data(service.get_allowed_municipalities())


class DepartmentAllowedMapWorksInfoSerializer(IDepartmentAllowedModuleSerializer):

    def get_allowed_categories(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.MAP_WORKS, department=instance)
        return WorkCategoryShortSerializer(service.get_allowed_categories(), many=True).data

    def get_allowed_municipalities(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.MAP_WORKS, department=instance)
        return get_divided_municipalities_data(service.get_allowed_municipalities())


class DepartmentAllowedPlansInfoSerializer(IDepartmentAllowedModuleSerializer):

    def get_allowed_categories(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.PLANS, department=instance)
        return PlansCategorySerializer(service.get_allowed_categories(), many=True).data

    def get_allowed_municipalities(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.PLANS, department=instance)
        return get_divided_municipalities_data(service.get_allowed_municipalities())


class DepartmentAllowedAppealsInfoSerializer(IDepartmentAllowedModuleSerializer):

    def get_allowed_categories(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.APPEALS, department=instance)
        return ProblematicSerializer(service.get_allowed_categories(), many=True).data

    def get_allowed_municipalities(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.APPEALS, department=instance)
        return get_divided_municipalities_data(service.get_allowed_municipalities())


class DepartmentAllowedEncouragementsInfoSerializer(IDepartmentAllowedModuleSerializer):

    def get_allowed_categories(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.ENCOURAGEMENTS, department=instance)
        return EncouragementsCategorySerializer(service.get_allowed_categories(), many=True).data

    def get_allowed_municipalities(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.ENCOURAGEMENTS, department=instance)
        return get_divided_municipalities_data(service.get_allowed_municipalities())


class DepartmentAllowedSuggestionsInfoSerializer(IDepartmentAllowedModuleSerializer):

    def get_allowed_categories(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.SUGGESTIONS, department=instance)
        return SuggestionsCategorySerializer(service.get_allowed_categories(), many=True).data

    def get_allowed_municipalities(self, instance: Department):
        service = self.department_service_factory.create(ModulesPermissions.SUGGESTIONS, department=instance)
        return get_divided_municipalities_data(service.get_allowed_municipalities())


class DepartmentAllowedFieldsInfoSerializer(serializers.Serializer):
    department_service = DepartmentService()
    locality_service = LocalityService()

    modules_permissions = serializers.ListSerializer(
        child=serializers.CharField(),
        source="sub_permissions.modules_permissions"
    )
    allowed_departments = serializers.SerializerMethodField()
    allowed_municipalities = serializers.SerializerMethodField()
    voting = serializers.SerializerMethodField()
    initiative = serializers.SerializerMethodField()
    map_works = serializers.SerializerMethodField()
    plans = serializers.SerializerMethodField()
    appeals = serializers.SerializerMethodField()
    encouragements = serializers.SerializerMethodField()
    suggestions = serializers.SerializerMethodField()

    def get_allowed_departments(self, instance: Department):
        departments = self.department_service.get_all_departments(instance)
        return DepartmentShortSerializer(departments, many=True).data

    def get_allowed_municipalities(self, instance: Department):
        municipalities_with_localities = instance.locality.all().order_by("name")

        return LocalitySerializer(municipalities_with_localities, many=True).data

    def get_voting(self, instance: Department):
        return DepartmentAllowedVotingInfoSerializer(instance).data

    def get_initiative(self, instance: Department):
        return DepartmentAllowedInitiativeInfoSerializer(instance).data

    def get_map_works(self, instance: Department):
        return DepartmentAllowedMapWorksInfoSerializer(instance).data

    def get_plans(self, instance: Department):
        return DepartmentAllowedPlansInfoSerializer(instance).data

    def get_appeals(self, instance: Department):
        return DepartmentAllowedAppealsInfoSerializer(instance).data

    def get_encouragements(self, instance: Department):
        return DepartmentAllowedEncouragementsInfoSerializer(instance).data

    def get_suggestions(self, instance: Department):
        return DepartmentAllowedSuggestionsInfoSerializer(instance).data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
