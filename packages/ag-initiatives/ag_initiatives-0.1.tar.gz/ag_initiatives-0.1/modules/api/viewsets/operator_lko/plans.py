from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.pagination import DefaultPagination
from modules.api.viewsets.operator_lko.serializers.locality import (
    MunicipalityWithUnavailableTreeSerializer,
    get_municipalities_with_unavailable_from_localities
)
from modules.api.viewsets.operator_lko.serializers.plan import (
    PlanOperatorLkoListSerializer
)
from modules.core.services.locality import LocalityService

from modules.plans.models import Plan, Location
from modules.plans.api.serializers import (
    PlanCreateSerializer,
    PlanDetailsSerializer,
    CategorySerializer,
    PlanCommentModeratorSerializer,
)
from modules.core.models import User
from modules.core.models.permissions import ModulesPermissions
from modules.core.services.operator_lko import OperatorLkoService
from modules.core.permissions import IsOperator


class PlanOperatorLkoAPI(viewsets.ModelViewSet):
    """API Планы Оператора ЛКО"""

    queryset = Plan.objects.none()
    permission_classes = [IsOperator]
    service_class = OperatorLkoService
    serializer_class = PlanOperatorLkoListSerializer
    pagination_class = DefaultPagination

    locality_service = LocalityService()

    def get_queryset(self):
        service = self.service_class(
            user=self.request.user, module=ModulesPermissions.PLANS)

        return Plan.objects.filter(
            locality__in=service.get_allowed_localities(),
            owner__in=service.get_allowed_departments(),
            category__in=service.get_allowed_categories(),
        ).distinct().order_by("-publication_date")

    def list(self, request: Request, *args, **kwargs):
        user: User = request.user
        service = self.service_class(user=user, module=ModulesPermissions.PLANS)
        paginator = self.pagination_class()

        plans = Plan.objects.filter(
            locality__in=service.get_allowed_localities(),
            owner__in=service.get_allowed_departments(),
            category__in=service.get_allowed_categories(),
        ).distinct().order_by("-publication_date")

        page = paginator.paginate_queryset(queryset=plans, request=request)
        serializer = self.serializer_class(page, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return response

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlanDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=True)
    def comments(self, request, pk=None, *args, **kwargs):
        plan: Plan = self.get_object()
        return Response(
            PlanCommentModeratorSerializer(
                plan.comments.filter(moderated=True), many=True
            ).data,
            status=status.HTTP_200_OK
        )

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user: User = request.user
        service = self.service_class(user=user, module=ModulesPermissions.PLANS)
        service.validate_plan_data(request.data)
        department = service.get_allowed_departments().pop()

        serializer = PlanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_data = serializer.validated_data

        location_data = plan_data.pop("location", None)
        location = None
        if location_data:
            location = Location.objects.create(**location_data)

        files = plan_data.pop("files")

        plan = Plan.objects.create(
            **plan_data,
            location=location,
            owner=department,
        )

        plan.files.set(files)

        return Response(
            PlanDetailsSerializer(plan).data, status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        user: User = request.user
        instance = self.get_object()

        service = self.service_class(user=user, module=ModulesPermissions.PLANS)
        service.validate_plan_data(request.data)

        serializer = PlanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_data = serializer.validated_data

        location_data = plan_data.pop("location")
        files = plan_data.pop("files")

        Location.objects.filter(pk=instance.location.pk).update(**location_data)

        Plan.objects.filter(pk=instance.pk).update(
            **plan_data,
        )

        instance.files.set(files)

        return Response(
            PlanDetailsSerializer(Plan.objects.get(pk=instance.pk)).data,
            status=status.HTTP_201_CREATED,
        )

    @action(methods=["get"], detail=False, url_path="info")
    def info(self, request: Request, *args, **kwargs):
        user: User = request.user
        service = self.service_class(user=user, module=ModulesPermissions.PLANS)

        # municipalities = get_municipalities_with_unavailable_from_localities(service.get_allowed_localities())
        municipalities = user.sub_permissions.operator_permissions.plans_localities.all()
        data = {
            "municipalities": MunicipalityWithUnavailableTreeSerializer(municipalities, many=True).data,
            "category": CategorySerializer(service.get_allowed_categories(), many=True).data
        }
        return Response(data)
