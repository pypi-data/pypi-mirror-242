from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.api.pagination import InitiativeCommunicationPagination
from modules.api.permissions import IsApplicant, IsModerator
from modules.api.serializers import (
    InitiativeOperatorCommunicationListSerializer,
    InitiativeCommunicationModerationSerializer,
)
from modules.initiatives.models import InitiativeOperatorCommunication, InitiativeState
from modules.initiatives.models.initiative_operator_communication import (
    ModerateResponseState,
)
from modules.initiatives.service.email_builder import EmailBuilder, EmailSender
from modules.initiatives.utils.mail_strings import EmailString


class InitiativeCommunicationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = InitiativeOperatorCommunicationListSerializer
    permission_classes = (IsApplicant,)
    queryset = (
        InitiativeOperatorCommunication.objects.select_related(
            "initiative",
            "user",
        )
        .prefetch_related("files")
        .order_by("-timestamp")
    )
    pagination_class = InitiativeCommunicationPagination

    def get_queryset(self):
        queryset = super(InitiativeCommunicationViewSet, self).get_queryset()
        if self.request.user.is_simple_user:
            return queryset.filter(
                Q(initiative__in=self.request.user.user_initiatives_for_actions)
                & ~Q(user=self.request.user)
            )
        elif self.request.user.is_moderator:
            return queryset.filter(
                Q(initiative__state=InitiativeState.MODERATION)
                & Q(state=ModerateResponseState.MODERATION_REQUIRED)
            )

    @action(
        methods=("PUT",),
        detail=True,
        permission_classes=(IsModerator,),
        url_path="moderate",
        url_name="moderate",
    )
    def moderate(self, request, pk=None):
        communication = self.get_object()
        serializer = InitiativeCommunicationModerationSerializer(
            instance=communication, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        template = (
            EmailString.MODERATOR_APPROVE_ANSWER
            if communication.state == ModerateResponseState.APPROVED
            else EmailString.MODERATOR_REJECT_ANSWER
        )
        email_builder = EmailBuilder(
            communication.initiative, user_template_string=template
        )
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()
        return Response()


class InitiativeCommunicationAPI(InitiativeCommunicationViewSet):
    pagination_class = LimitOffsetPagination
