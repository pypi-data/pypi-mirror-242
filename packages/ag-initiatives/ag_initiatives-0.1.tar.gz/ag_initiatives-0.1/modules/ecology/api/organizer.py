from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.core.models import User
from modules.core.permissions import IsOperator
from modules.ecology.api.serializers import (
    ParticipationListSerializer,
    ParticipationSerializer,
)
from modules.ecology.api.serializers.participation import (
    ParticipationOrganizerExcelSerializer,
)
from modules.ecology.models import ParticipationUserEvent
from modules.ecology.models.participation_user_event import ParticipationStatus
from modules.ecology.pagination import DefaultPagination
from modules.ecology.services import OrganizerService
from modules.ecology.exceptions import BalanceOperationError
from modules.ecology.services.organizer_service import OrganizerError


class OrganizerParticipationAPI(viewsets.ViewSet):

    permission_classes = [IsOperator]

    def list(self, request):
        organizer: User = request.user

        try:
            queryset = OrganizerService(organizer).get_users_participation()
        except OrganizerError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        paginator = DefaultPagination()
        page = paginator.paginate_queryset(queryset, request=request)
        response = paginator.get_paginated_response(
            ParticipationListSerializer(page, many=True).data
        )
        return response

    def retrieve(self, request, pk=None):
        participation = ParticipationUserEvent.objects.filter(pk=pk).first()

        if not participation:
            return Response(
                "Участие в предложении не найдено", status=status.HTTP_400_BAD_REQUEST
            )
        if not (participation.status == ParticipationStatus.NOT_CONFIRMED):
            return Response(
                "Участие уже подтверждено или отклонено",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ParticipationSerializer(instance=participation)
        return Response(serializer.data)

    def partial_update(self, request, pk):
        organizer: User = request.user

        participation = ParticipationUserEvent.objects.filter(pk=pk).first()
        if not participation:
            return Response(
                "Участие в предложении не найдено", status=status.HTTP_400_BAD_REQUEST
            )

        participation_status = request.data["status"]

        try:
            OrganizerService(organizer).confirm_or_decline_participation(
                participation=participation, participation_status=participation_status
            )
        except (OrganizerError, BalanceOperationError) as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(ParticipationSerializer(participation).data)

    @action(methods=["get"], detail=False)
    def excel(self, request):
        organizer: User = request.user

        queryset = OrganizerService(organizer).get_users_participation()

        json_data = ParticipationOrganizerExcelSerializer(queryset, many=True).data
        return ParticipationOrganizerExcelSerializer.excel_response(
            json_data, response_status=status.HTTP_200_OK
        )
