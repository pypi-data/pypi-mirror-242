from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.api.serializers import LocalitySerializer
from modules.core.models import User
from modules.core.permissions import IsOperator
from modules.map_works.api.filters import WorksFilter
from modules.map_works.api.serializers import (
    WorksCreateSerializer,
    WorksListSerializer,
    WorksList2Serializer,
    WorkCategorySerializer,
)
from modules.map_works.models import Works, Location

class WorksOperatorAPI(viewsets.ModelViewSet):
    queryset = Works.objects.none()
    serializer_class = WorksListSerializer
    filterset_class = WorksFilter
    permission_classes = [IsOperator]

    def get_queryset(self):
        user: User = self.request.user
        if not user.department:
            return Works.objects.none()
        return Works.objects.filter(owner=user.department)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WorksList2Serializer
        if self.action == "update":
            return WorksList2Serializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

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
            WorkCategorySerializer(
                [v.category for v in request.user.department.works_categories.all()],
                many=True,
            ).data
        )

    @transaction.atomic
    @action(methods=["post"], detail=False)
    def add(self, request):
        user: User = request.user

        serializer = WorksCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        works_data = serializer.validated_data

        locations = works_data.pop("locations")

        # todo: избавиться от копипасты
        if not user.department:
            return Response(
                "Ошибка добавления. У пользователя не определено ведомство",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.department.locality.filter(pk=works_data["locality"].pk).exists():
            return Response(
                "Ошибка добавления. МО нет в списке ведомства пользователя",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.department.works_categories.filter(
            category=works_data["category"]
        ).exists():
            return Response(
                "Ошибка добавления. Для ведомства пользователя не назначено выбранной категории",
                status=status.HTTP_400_BAD_REQUEST,
            )

        works = Works.objects.create(
            **works_data,
            owner=user.department,
            is_published=True,
        )

        for location in locations:
            Location.objects.create(work=works, **location)

        return Response(
            WorksList2Serializer(works).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        user: User = request.user
        partial = kwargs.pop("partial", False)
        if partial:
            Response(status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # todo: избавиться от копипасты
        if not user.department:
            return Response(
                "Ошибка добавления. У пользователя не определено ведомство",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.department.locality.filter(
            pk=serializer.validated_data["locality"].pk
        ).exists():
            return Response(
                "Ошибка добавления. МО нет в списке ведомства пользователя",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.department.works_categories.filter(
            category=serializer.validated_data["category"]
        ).exists():
            return Response(
                "Ошибка добавления. Для ведомства пользователя не назначено выбранной категории",
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_update(serializer)

        return Response(serializer.data)
