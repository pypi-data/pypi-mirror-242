from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.core.permissions import IsAdminLKO, IsOperator
from modules.voting.api.filters import VotingParticipantFilter
from modules.voting.api.serializers import VotingParticipantSerializer
from modules.voting.models import VotingParticipant
from modules.voting.services.voting_participant_service import VotingParticipantService


class VotingParticipantAPI(viewsets.ModelViewSet):
    queryset = VotingParticipant.objects.all()
    serializer_class = VotingParticipantSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = VotingParticipantFilter
    permission_classes = [IsAdminLKO | IsOperator]
    pagination_class = LimitOffsetPagination
    service = VotingParticipantService(queryset, serializer_class)

    @action(methods=["post"], detail=False)
    def from_user(self, request):
        user_pk = request.data.get("user_pk")
        if not user_pk:
            raise ValidationError("user_pk is empty")
        comment = request.data.get("comment")
        data = self.service.create_voting_participant_from_user(user_pk, comment)
        return Response(data, status.HTTP_201_CREATED)

    class Meta:
        model = VotingParticipant
