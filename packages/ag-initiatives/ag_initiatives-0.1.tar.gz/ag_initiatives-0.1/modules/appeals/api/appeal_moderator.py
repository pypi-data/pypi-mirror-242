from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status

from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.appeals.api.filters import AppealFilter
from modules.appeals.api.serializers import (
    AppealModeratorListSerializer,
    AppealModeratorDetailsSerializer,
    RejectAppealModeratorSerializer,
    AppealSetAddressModeratorSerializer,
    RejectReasonSerializer,
    AppealStateChangeShortSerializer,
    AppealOwnerCommunicationsModeratorSerializer,
    AppealOwnerCommunicationsModeratorCreateSerializer,
)
from modules.appeals.models import (
    Appeal,
    AppealState,
    RejectReason,
    DepartmentCategory,
    AppealStateChange,
    AppealOwnerCommunicationType,
)
from modules.appeals.services.mail_service import MailService
from modules.core.permissions import IsModerator


class AppealModeratorAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Appeal.objects.none()
    serializer_class = AppealModeratorListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AppealFilter
    permission_classes = [IsModerator]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return (
            Appeal.objects.filter(
                state=AppealState.MODERATION,
            )
            .order_by("-creation_date_time")
            .select_related(
                "locality",
                "category",
                "category__parent",
            )
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AppealModeratorDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    @action(methods=["get"], detail=False)
    def reject_reasons(self, request):
        return Response(
            RejectReasonSerializer(RejectReason.objects.all(), many=True).data
        )

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def accept(self, request, pk):
        instance: Appeal = self.get_object()

        if instance.address == "":
            return Response("Не заполнен адрес", status=status.HTTP_400_BAD_REQUEST)

        if DepartmentCategory.objects.filter(category=instance.category).count() == 0:
            return Response(
                "На категорию обращения не назначено ведомства",
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.moderator_accept()
        instance.save(update_fields=["state", "moderation_pass_date"])

        AppealStateChange.objects.create(
            appeal=instance,
            new_state=instance.state,
            user=request.user,
            department=request.user.department,
        )

        MailService.notify_user_accepted(instance)
        MailService.notify_operator_accepted(instance)

        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def reject(self, request, pk):
        instance: Appeal = self.get_object()
        serializer = RejectAppealModeratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reject_data = serializer.validated_data
        reason_id = reject_data.pop("reason_id", None)
        reason_text_first = ""
        reason_text_second = reject_data.pop("reason_text", "")

        if reason_id is None and (
            reason_text_second is None or reason_text_second == ""
        ):
            return Response(
                "Не указана причина отказа", status=status.HTTP_400_BAD_REQUEST
            )

        if reason_id is not None:
            reason = RejectReason.objects.get(pk=reason_id)
            reason_text_first = reason.text

        instance.moderator_reject()
        instance.save(update_fields=["state", "moderation_pass_date"])

        AppealStateChange.objects.create(
            appeal=instance,
            new_state=instance.state,
            comment=reason_text_first,
            second_comment=reason_text_second,
            user=request.user,
            department=request.user.department,
        )

        MailService.notify_user_rejected(
            instance, reason_text_first + " " + reason_text_second
        )

        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def set_address(self, request, pk):
        instance: Appeal = self.get_object()
        serializer = AppealSetAddressModeratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if instance.state != AppealState.MODERATION:
            return Response(
                "Обращение не в состоянии модерации", status=status.HTTP_400_BAD_REQUEST
            )

        instance.address = serializer.validated_data["address"]
        instance.save(update_fields=["address"])
        return Response(status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True, url_path="notifications")
    def item_notifications(self, request, pk):
        instance: Appeal = self.get_object()
        queryset = AppealStateChange.objects.filter(appeal=instance).order_by(
            "-timestamp"
        )
        return Response(AppealStateChangeShortSerializer(queryset, many=True).data)

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def make_user_request(self, request, pk):
        instance: Appeal = self.get_object()

        if instance.state != AppealState.MODERATION:
            return Response(
                'Невозможно сформировать запрос. Обращение не в статусе "На модерации"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AppealOwnerCommunicationsModeratorCreateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        res = serializer.save(
            appeal=instance,
            timestamp=timezone.now(),
            type=AppealOwnerCommunicationType.REQUEST,
        )

        MailService.notify_user_moderation_request(instance)

        return Response(status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True)
    def requests(self, request, pk):
        instance: Appeal = self.get_object()
        return Response(
            AppealOwnerCommunicationsModeratorSerializer(
                instance.owner_communications.all().order_by("-timestamp"), many=True
            ).data
        )
