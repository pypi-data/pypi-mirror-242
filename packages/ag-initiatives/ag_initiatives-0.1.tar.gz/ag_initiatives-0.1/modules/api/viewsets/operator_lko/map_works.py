from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.pagination import DefaultPagination
from modules.api.viewsets.filters.map_works import MapWorksFilter
from modules.api.viewsets.operator_lko.serializers.locality import \
    get_municipalities_with_unavailable_from_localities, \
    MunicipalityWithUnavailableTreeSerializer
from modules.api.viewsets.operator_lko.serializers.map_works import \
    WorksOperatorLkoListSerializer, \
    WorksOperatorLkoDetailSerializer
from modules.core.models import User
from modules.core.models.permissions import ModulesPermissions
from modules.core.permissions import IsOperator
from modules.core.services.operator_lko import OperatorLkoService
from modules.map_works.api.serializers import (
    WorksCreateSerializer,
    WorkTypeSerializer,
    ContractorSerializer,
    WorkReasonSerializer,
    InstitutionTypeSerializer, WorkCategorySerializer,
)
from modules.map_works.models import (
    Works,
    Location,
    WorkType,
    Contractor,
    WorkReason,
    InstitutionType,
)


class MapWorksOperatorLkoAPI(viewsets.ModelViewSet):
    """API Оператор ЛКО Карта Запланированных работы"""
    queryset = Works.objects.none()
    permission_classes = [IsOperator]
    service_class = OperatorLkoService
    serializer_class = WorksOperatorLkoListSerializer
    pagination_class = DefaultPagination
    filterset_class = MapWorksFilter

    def get_queryset(self):
        service = self.service_class(user=self.request.user,
                                     module=ModulesPermissions.MAP_WORKS)

        return Works.objects.filter(
            locality__in=service.get_allowed_localities(),
            owner__in=service.get_allowed_departments(),
            category__in=service.get_allowed_categories(),
        ).distinct().order_by("id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WorksOperatorLkoDetailSerializer
        return self.serializer_class

    def list(self, request: Request, *args, **kwargs):
        user: User = request.user
        service = self.service_class(user=user,
                                     module=ModulesPermissions.MAP_WORKS)
        paginator = self.pagination_class()

        works = Works.objects.filter(
            locality__in=service.get_allowed_localities(),
            owner__in=service.get_allowed_departments(),
            category__in=service.get_allowed_categories(),
        ).distinct().order_by("id")

        filtered_queryset = self.filterset_class(data=request.query_params,
                                                 queryset=works).qs

        page = paginator.paginate_queryset(queryset=filtered_queryset,
                                           request=request)
        serializer = self.serializer_class(page, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return response

    @transaction.atomic
    def create(self, request):
        user: User = request.user
        service = self.service_class(user=user,
                                     module=ModulesPermissions.MAP_WORKS)
        service.validate_map_works_data(request.data)
        department = service.get_allowed_departments().pop()

        serializer = WorksCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        works_data = serializer.validated_data

        locations = works_data.pop("locations")

        works = Works.objects.create(
            **works_data,
            owner=department,
            is_published=True,
        )

        for location in locations:
            Location.objects.create(work=works, **location)

        return Response(
            WorksOperatorLkoDetailSerializer(works).data,
            status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        user: User = request.user
        service = self.service_class(user=user,
                                     module=ModulesPermissions.MAP_WORKS)
        service.validate_map_works_data(request.data)

        instance = self.get_object()
        serializer = WorksCreateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        works_data = serializer.validated_data

        locations = works_data.pop("locations")
        instance.locations.all().delete()

        serializer.save()

        for location in locations:
            Location.objects.create(work=instance, **location)

        return Response(WorksOperatorLkoDetailSerializer(instance).data)

    @action(methods=["get"], detail=False, url_path="info")
    def info(self, request: Request, *args, **kwargs):
        user: User = request.user
        service = self.service_class(
            user=user,
            module=ModulesPermissions.MAP_WORKS
        )
        municipalities = user.sub_permissions.operator_permissions.map_works_localities.all()

        data = {
            "municipalities": MunicipalityWithUnavailableTreeSerializer(
                municipalities, many=True).data,
            "category": WorkCategorySerializer(
                service.get_allowed_categories(), many=True).data,
            "work_type": WorkTypeSerializer(
                WorkType.objects.all(), many=True).data,
            "contractor": ContractorSerializer(
                Contractor.objects.all(), many=True).data,
            "reason": WorkReasonSerializer(
                WorkReason.objects.all(), many=True).data,
            "institution_type": InstitutionTypeSerializer(
                InstitutionType.objects.all(), many=True).data
        }
        return Response(data)

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response(
            {"count": self.filter_queryset(self.get_queryset()).count()})
