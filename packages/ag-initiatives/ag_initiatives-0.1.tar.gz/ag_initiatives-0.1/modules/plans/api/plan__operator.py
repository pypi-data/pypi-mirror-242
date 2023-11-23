from django.db import transaction
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.api.serializers import LocalitySerializer
from modules.core.models import User
from modules.core.permissions import IsOperator
from modules.plans.api.filters import PlanFilter
from modules.plans.api.serializers import (
    PlanListSerializer,
    PlanDetailsSerializer,
    PlanCreateSerializer,
    CategoryDetailedSerializer,
    PlanDetails2Serializer,
    PlanCommentModeratorSerializer,
)
from modules.plans.models import Plan, Location


class PlanOperatorAPI(viewsets.ModelViewSet):
    queryset = Plan.objects.none()
    serializer_class = PlanListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PlanFilter
    pagination_class = LimitOffsetPagination
    permission_classes = [IsOperator]

    def get_queryset(self):
        user: User = self.request.user
        if not user.department:
            return Plan.objects.none()
        return Plan.objects.filter(owner=user.department).order_by("-publication_date")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlanDetails2Serializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    @action(methods=["get"], detail=True)
    def details(self, request, pk):
        return Response(PlanDetailsSerializer(self.get_object()).data)

    @action(methods=["get"], detail=False)
    def localities(self, request):
        return Response(
            LocalitySerializer(
                request.user.department.locality.all().order_by("order", "name"),
                many=True,
            ).data
        )

    @action(methods=["get"], detail=False)
    def categories(self, request):
        return Response(
            CategoryDetailedSerializer(
                [v.category for v in request.user.department.plans_categories.all()],
                many=True,
            ).data
        )

    @action(methods=["get"], detail=True)
    def comments(self, request, pk=None, *args, **kwargs):
        plan: Plan = self.get_object()
        return Response(
            PlanCommentModeratorSerializer(
                plan.comments.filter(moderated=True), many=True
            ).data,
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user: User = request.user

        serializer = PlanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_data = serializer.validated_data

        location_data = plan_data.pop("location")

        # todo: избавиться от копипасты
        if not user.department:
            return Response(
                "Ошибка добавления. У пользователя не определено ведомство",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.department.locality.filter(pk=plan_data["locality"].pk).exists():
            return Response(
                "Ошибка добавления. МО нет в списке ведомства пользователя",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.department.plans_categories.filter(
            category=plan_data["category"]
        ).exists():
            return Response(
                "Ошибка добавления. Для ведомства пользователя не назначено выбранной категории",
                status=status.HTTP_400_BAD_REQUEST,
            )

        location = Location.objects.create(**location_data)

        files = plan_data.pop("files")

        plan = Plan.objects.create(
            **plan_data,
            location=location,
            owner=user.department,
        )

        plan.files.set(files)

        return Response(
            PlanDetails2Serializer(plan).data, status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        user: User = request.user
        instance = self.get_object()

        serializer = PlanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_data = serializer.validated_data

        location_data = plan_data.pop("location")
        files = plan_data.pop("files")

        # todo: избавиться от копипасты
        if not user.department:
            return Response(
                "Ошибка добавления. У пользователя не определено ведомство",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.department.locality.filter(pk=plan_data["locality"].pk).exists():
            return Response(
                "Ошибка добавления. МО нет в списке ведомства пользователя",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.department.plans_categories.filter(
            category=plan_data["category"]
        ).exists():
            return Response(
                "Ошибка добавления. Для ведомства пользователя не назначено выбранной категории",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if instance.location:
            Location.objects.filter(pk=instance.location.pk).update(**location_data)

        Plan.objects.filter(pk=instance.pk).update(
            **plan_data,
        )

        instance.files.set(files)

        return Response(
            PlanDetails2Serializer(Plan.objects.get(pk=instance.pk)).data,
            status=status.HTTP_201_CREATED,
        )
