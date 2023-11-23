from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, permissions, status

from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.appeals.api.filters import AppealFilter
from modules.appeals.api.serializers import (
    AppealCreateSerializer,
    AppealUserListSerializer,
    AppealUserDetailsSerializer,
    AppealDetailsSerializer,
    AppealStateChangeSerializer,
    AppealStateChangeShortSerializer,
    AppealOwnerCommunicationsUserSerializer,
    AppealOwnerCommunicationsUserCreateSerializer,
)
from modules.appeals.models import (
    Appeal,
    AppealState,
    AppealStateChange,
    AppealOwnerCommunicationType,
)
from modules.core.models import User
from modules.core.permissions import IsUser


class AppealUserAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Appeal.objects.none()
    serializer_class = AppealUserListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AppealFilter
    permission_classes = [IsUser]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AppealUserDetailsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return (
            Appeal.objects.filter(user=self.request.user)
            .select_related(
                "locality",
                "category",
                "category__parent",
            )
            .order_by("-creation_date_time")
        )

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    @transaction.atomic
    @action(methods=["post"], detail=False)  # , permission_classes=[IsUser]
    def add(self, request):
        user: User = request.user
        esia_verified = user.esia_verified
        user_age = user.age
        user_locality = user.get_locality_for_initiative()

        serializer = AppealCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appeal_data = serializer.validated_data
        files = appeal_data.pop("files", None)

        if esia_verified is None or not esia_verified:
            return Response(
                "Учетная запись ЕСИА не подтверждена",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_age is None:
            return Response(
                "В учетной записи ЕСИА не указана дата рождения",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_age < 14:
            return Response(
                "Возраст не соответствует условиям подачи инициатиы",
                status=status.HTTP_400_BAD_REQUEST,
            )

        appeal = Appeal.objects.create(
            number="", user=user, state=AppealState.MODERATION, **appeal_data
        )

        if files is not None:
            appeal.files.set(files)
        appeal.number = f"О-{appeal.pk:0>10d}"
        appeal.save(update_fields=["number"])

        AppealStateChange.objects.create(appeal=appeal, new_state=appeal.state)

        return Response(
            AppealUserDetailsSerializer(appeal).data, status=status.HTTP_201_CREATED
        )

    @action(methods=["get"], detail=False)
    def notifications(self, request):
        queryset = AppealStateChange.objects.filter(appeal__user=request.user).order_by(
            "-timestamp"
        )
        return Response(AppealStateChangeSerializer(queryset, many=True).data)

    @action(methods=["get"], detail=True, url_path="notifications")
    def item_notifications(self, request, pk):
        instance: Appeal = self.get_object()
        queryset = AppealStateChange.objects.filter(appeal=instance).order_by(
            "-timestamp"
        )
        return Response(AppealStateChangeShortSerializer(queryset, many=True).data)

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def make_moderator_response(self, request, pk):
        instance: Appeal = self.get_object()

        if instance.state != AppealState.MODERATION:
            return Response(
                'Невозможно сформировать ответ. Обращение не в статусе "На модерации"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        if instance.owner_communications.count() == 0:
            return Response(
                "Невозможно сформировать ответ. Нет запроса от модератора.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AppealOwnerCommunicationsUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        res = serializer.save(
            appeal=instance,
            timestamp=timezone.now(),
            type=AppealOwnerCommunicationType.RESPONSE,
        )

        return Response(status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True)
    def responses(self, request, pk):
        instance: Appeal = self.get_object()
        return Response(
            AppealOwnerCommunicationsUserSerializer(
                instance.owner_communications.all().order_by("-timestamp"), many=True
            ).data
        )
