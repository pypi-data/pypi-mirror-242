from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Q, Prefetch
from django_filters import rest_framework as filters
from django_fsm import TransitionNotAllowed
from rest_framework import status, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from modules.api.filters import InitiativeFilter
from modules.api.permissions import (
    IsInitiativeModerator,
    IsAllowedToAcceptOrRejectChanges,
    IsInitiativeOperator,
    IsOperatorAllowedToRequestInfo,
    IsInitiativeApplicant,
    IsOperatorAllowedToView,
    IsApplicantAllowedToAnswer,
)
from modules.api.permissions.initiative_moderator_permission import (
    IsModeratorAllowedToOfferChanges,
    IsModeratorAllowedToRequestInfo,
)
from modules.api.serializers import (
    InitiativeUpdateSerializer,
    CommunicationReasonFilesSerializer,
    InitiativeForUserSerializer,
    MessagingRequestSerializer,
    CommunicationTextFilesSerializer,
    MessagingResponseSerializer,
    InitiativePDFSerializer,
    InitiativePrivateSerializer,
    InitiativeCategoryAvailableSerializer,
)
from modules.core.mixins.user_track_admin import TrackUserApiMixin
from modules.core.models import User
from modules.ecology.exceptions import UserError, BalanceOperationError
from modules.ecology.models import UserState
from modules.initiatives.enums import InitiativeState
from modules.initiatives.models import (
    Initiative,
    InitiativeAcceptingSettings,
    InitiativeCategory,
)
from modules.initiatives.service.email_builder import EmailBuilder, EmailSender
from modules.initiatives.service.pdf_builder import build_pdf
from modules.initiatives.utils import save_initiative_old_data
from modules.initiatives.utils.initiative_initial_data_manipulation import (
    restore_initiative_initial_data,
)
from modules.initiatives.utils.mail_strings import EmailString
from modules.ecology.services.user_service import UserService as EcologyUserService


class InitiativePrivateAPI(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Initiative.objects.select_related(
        "category", "category__parent"
    ).prefetch_related('locality')
    serializer_class = InitiativePrivateSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InitiativeFilter
    permission_classes = [
        IsInitiativeOperator
        | IsInitiativeModerator
        | IsInitiativeApplicant
        | IsOperatorAllowedToView
    ]

    @action(
        methods=("GET",), detail=False, permission_classes=[permissions.IsAuthenticated]
    )
    def my_list(self, request):
        user: User = request.user
        return Response(
            InitiativeForUserSerializer(
                user.user_initiatives_for_view, user=user, many=True
            ).data
        )

    @action(
        methods=("GET",),
        detail=True,
        url_path="pdf",
        url_name="pdf",
        permission_classes=(IsOperatorAllowedToView,),
    )
    def initiative_to_pdf(self, request, pk=None):
        initiative = self.get_object()
        filename, output = build_pdf(InitiativePDFSerializer(initiative).data)
        initiative.pdf_export.save(filename, ContentFile(output))
        return Response({"link": initiative.pdf_export.url})

    @action(
        methods=("GET",),
        detail=True,
        url_path="available-categories",
        url_name="available-categories",
        permission_classes=(IsInitiativeModerator,),
    )
    def get_available_categories(self, request, pk=None):
        initiative = self.get_object()
        settings = InitiativeAcceptingSettings.objects.filter(
            locality__in=initiative.locality.all(), active=True
        ).values_list("category", flat=True)
        base = (
            InitiativeCategory.objects.filter(
                Q(parent__isnull=True) & Q(children__in=settings)
            )
            .prefetch_related(
                Prefetch(
                    "children",
                    queryset=InitiativeCategory.objects.filter(id__in=settings),
                )
            )
            .distinct()
        )
        return Response(InitiativeCategoryAvailableSerializer(base, many=True).data)

    @action(
        methods=("POST",),
        detail=True,
        url_path="reject-user",
        url_name="reject-user",
        permission_classes=(IsAllowedToAcceptOrRejectChanges,),
    )
    def user_reject_changes(self, request, pk=None):
        initiative = self.get_object()
        try:
            with transaction.atomic():
                initiative.user_reject_changes(request.user)
                restore_initiative_initial_data(initiative, InitiativeUpdateSerializer)
                initiative.save()
                TrackUserApiMixin.create(request, initiative, None, True)
        except TransitionNotAllowed:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(initiative.state)

    @action(
        methods=("POST",),
        detail=True,
        url_path="reject-moderator",
        url_name="reject-moderator",
        permission_classes=(IsInitiativeModerator,),
    )
    def moderator_reject(self, request, pk=None):
        initiative = self.get_object()
        serializer = CommunicationReasonFilesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                with transaction.atomic():
                    initiative.moderator_reject(request.user, serializer.validated_data)
                    initiative.save()
                    TrackUserApiMixin.create(request, initiative, None, True)
            except TransitionNotAllowed:
                return Response(status=status.HTTP_403_FORBIDDEN)
            return Response(initiative.state)

    @action(
        methods=("POST",),
        detail=True,
        url_path="accept-moderator",
        url_name="accept-moderator",
        permission_classes=(IsInitiativeModerator,),
    )
    def moderator_accept(self, request, pk=None):
        initiative = self.get_object()
        try:
            with transaction.atomic():
                initiative.moderator_accept(request.user)
                initiative.save()
                TrackUserApiMixin.create(request, initiative, None, True)
        except TransitionNotAllowed:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(initiative.state)

    @action(
        methods=("PUT",),
        detail=True,
        url_path="change-moderator",
        url_name="change-moderator",
        permission_classes=(IsModeratorAllowedToOfferChanges,),
    )
    def moderator_change_initiative(self, request, pk=None):
        initiative = self.get_object()
        serializer = InitiativeUpdateSerializer(instance=initiative, data=request.data)
        serializer.is_valid(raise_exception=True)
        save_initiative_old_data(initiative, serializer.validated_data)
        serializer.save()
        try:
            with transaction.atomic():
                initiative.moderator_offer_changes(request.user, serializer.data)
                initiative.save()
                TrackUserApiMixin.create(request, initiative, None, True)
        except TransitionNotAllowed:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data)

    @action(
        methods=("POST",),
        detail=True,
        url_path="response-info",
        url_name="response-info",
        permission_classes=(IsApplicantAllowedToAnswer,),
    )
    def response_info(self, request, pk=None):
        initiative = self.get_object()
        initiative.state = InitiativeState.PREMODERATION
        initiative.save()
        serializer = MessagingResponseSerializer(
            data=request.data, context={"initiative": initiative, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.create(serializer.validated_data)
        email_builder = EmailBuilder(
            initiative, operator_template_string=EmailString.ADDITIONAL_INFO_RESPONSE
        )
        email_sender = EmailSender(email_builder)
        email_sender.send_to_department_if_notifications_enabled()
        return Response(status=status.HTTP_201_CREATED)

    @action(
        methods=("POST",),
        detail=True,
        url_path="request-info",
        url_name="request-info",
        permission_classes=[
            IsModeratorAllowedToRequestInfo | IsOperatorAllowedToRequestInfo
        ],
    )
    def request_info(self, request, pk=None):
        initiative = self.get_object()
        serializer = MessagingRequestSerializer(
            data=request.data, context={"initiative": initiative, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.create(serializer.validated_data)
        email_string = (
            EmailString.ADDITIONAL_INFO_REQUEST_MODERATOR
            if request.user.is_moderator
            else EmailString.ADDITIONAL_INFO_REQUEST_OPERATOR
        )

        email_builder = EmailBuilder(initiative, user_template_string=email_string)
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()
        return Response(status=status.HTTP_201_CREATED)

    @action(
        methods=("POST",),
        detail=True,
        url_path="accept-user",
        url_name="accept-user",
        permission_classes=(IsAllowedToAcceptOrRejectChanges,),
    )
    def user_accept_changes(self, request, pk=None):
        initiative = self.get_object()
        try:
            with transaction.atomic():
                initiative.user_accept_changes(request.user)
                initiative.save()
                TrackUserApiMixin.create(request, initiative, None, True)
        except TransitionNotAllowed:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(initiative.state)

    @action(
        methods=("POST",),
        detail=True,
        url_path="reject-operator",
        url_name="reject-operator",
        permission_classes=(IsInitiativeOperator,),
    )
    def operator_reject(self, request, pk=None):
        initiative = self.get_object()
        serializer = CommunicationTextFilesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                initiative.operator_reject(
                    user=request.user, validated_data=serializer.validated_data
                )
                initiative.save()
                TrackUserApiMixin.create(request, initiative, None, True)
        except TransitionNotAllowed:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(initiative.state)

    @action(
        methods=("POST",),
        detail=True,
        url_path="accept-operator",
        url_name="accept-operator",
        permission_classes=(IsInitiativeOperator,),
    )
    def operator_accept(self, request, pk=None):
        initiative = self.get_object()
        try:
            with transaction.atomic():
                initiative.operator_accept(request.user)
                initiative.save()
                TrackUserApiMixin.create(request, initiative, None, True)
        except TransitionNotAllowed:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Добавляем бонусы в разделе экологии
        try:
            initiative_user: User = initiative.user
            if (
                initiative_user.ecology.state != UserState.INITIAL
                and initiative_user.is_simple_user
            ):
                EcologyUserService(
                    initiative_user
                ).add_bonuses_on_user_adding_initiative(initiative)
        except (UserError, BalanceOperationError):
            pass
        return Response(initiative.state)

    @action(
        methods=("POST",),
        detail=True,
        url_path="publish",
        url_name="publish",
        permission_classes=(IsInitiativeOperator,),
    )
    def operator_publish_decision(self, request, pk=None):
        initiative = self.get_object()
        serializer = CommunicationTextFilesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                initiative.publish_decision(request.user, serializer.validated_data)
                initiative.save()
                TrackUserApiMixin.create(request, initiative, None, True)
        except TransitionNotAllowed:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(initiative.state)

    @action(
        methods=("POST",),
        detail=True,
        url_path="accomplish",
        url_name="accomplish",
        permission_classes=(IsInitiativeOperator,),
    )
    def operator_accomplish(self, request, pk=None):
        initiative = self.get_object()
        serializer = CommunicationTextFilesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                initiative.accomplished(request.user, serializer.validated_data)
                initiative.save()
                TrackUserApiMixin.create(request, initiative, None, True)
        except TransitionNotAllowed:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(initiative.state)
