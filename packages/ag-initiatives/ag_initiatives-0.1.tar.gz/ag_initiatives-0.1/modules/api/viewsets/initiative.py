from des.models import DynamicEmailConfiguration
from django.db import transaction
from django.db.models import Prefetch, Q
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.api.filters import InitiativeFilter
from modules.api.serializers import (
    InitiativeSerializer,
    InitiativeShortSerializer,
    InitiativeCreateSerializer,
)
from modules.core.mixins.user_track_admin import TrackUserApiMixin
from modules.core.models import User, UserRole, Locality
from modules.ecology.models import UserState
from modules.ecology.services.user_service import \
    UserService as EcologyUserService
from modules.initiatives.enums import InitiativeTypes
from modules.initiatives.models import (
    Initiative,
    InitiativeState,
    InitiativeFile,
    UserInitiativeApprove,
    InitiativeAcceptingSettings,
    InitiativeOperatorCommunication,
    InitiativeOperatorCommunicationType,
    InitiativeSettings,
    InitiativeStateChange,
)
from modules.initiatives.service.email_builder import EmailBuilder, EmailSender
from modules.initiatives.tasks import send_email_initiative_broadcast
from modules.initiatives.utils.mail_strings import EmailString


class InitiativeAPI(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Initiative.objects.filter(
            state__in=[
                InitiativeState.VOTES_COLLECTION,
                InitiativeState.REJECTED_VOTES_THRESHOLD,
                InitiativeState.CONSIDERATION,
                InitiativeState.IN_PROGRESS,
                InitiativeState.ACCOMPLISHED,
            ]
        )
        .order_by("-creation_date_time")
        .prefetch_related(
            Prefetch(
                "files",
                queryset=InitiativeFile.objects.order_by("type", "order")
            ),
            Prefetch(
                "initiative_operator_communication",
                queryset=InitiativeOperatorCommunication.objects.filter(
                    type__in=[
                        InitiativeOperatorCommunicationType.IN_PROGRESS_NOTIFICATION,
                        InitiativeOperatorCommunicationType.ACCOMPLISHED_NOTIFICATION,
                    ]
                ),
            ),
            'locality',
        )
    )
    serializer_class = InitiativeShortSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InitiativeFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return InitiativeSerializer
        return super().get_serializer_class()

    @transaction.atomic
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def add(self, request):
        user: User = request.user
        esia_verified = user.esia_verified
        user_age = user.age
        user_locality = user.get_locality_for_initiative()
        settings: InitiativeSettings = InitiativeSettings.load()

        serializer = InitiativeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        initiative_data = serializer.validated_data
        files = initiative_data.pop("files", None)
        is_regional = initiative_data.pop("is_regional", False)
        initiative_settings: InitiativeAcceptingSettings = initiative_data.get(
            "settings"
        )

        if not initiative_settings.active:
            return Response(
                "Настройка категории неактивна",
                status=status.HTTP_400_BAD_REQUEST,
            )

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

        if settings.user_locality_check:
            if user_locality is None:
                return Response(
                    "В учетной записи ЕСИА не указан адрес проживания/регистрации",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not initiative_settings.locality.filter(
                Q(parent=user_locality) |
                Q(id=user_locality.id) |
                Q(localities=user_locality)
            ).exists():
                return Response(
                    "Муниципальное образование инициативы не соответствует адресу проживания/регистрации указанному в учетной записи ЕСИА",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        now_time = timezone.now()

        initiative = Initiative.objects.create(
            number="",
            creation_date_time=now_time,
            user=user,
            category=initiative_settings.category,
            duration_month=initiative_settings.duration_month,
            votes_threshold=initiative_settings.votes_threshold,
            state=InitiativeState.PREMODERATION,
            **initiative_data,
        )
        if is_regional:
            initiative.type = InitiativeTypes.REGIONAL
            initiative.locality.set(
                Locality.objects.all().values_list('id', flat=True)
            )
        else:
            initiative.type = InitiativeTypes.MUNICIPAL
            initiative.locality.set(initiative_settings.locality.all())
        if files is not None:
            initiative.files.set(files)
        initiative.number = f"И-{initiative.pk:0>10d}"
        initiative.save(update_fields=["number"])
        TrackUserApiMixin.create(request, initiative, None, False)
        InitiativeStateChange.objects.create(
            initiative=initiative,
            new_state=InitiativeState.PREMODERATION,
            timestamp=now_time,
        )

        InitiativeOperatorCommunication.objects.create(
            initiative=initiative,
            timestamp=now_time,
            type=InitiativeOperatorCommunicationType.SYSTEM_NOTIFICATION,
            text="Инициатива зарегистрирована",
        )

        if initiative_settings.department.email_initiative_notification:
            mail_content = {
                "subject": "Поступила новая инициатива на модерацию",
                "text": f'Инициатива «{initiative.number}, "{initiative.title}"» поступила на модерацию',
                "to_mail": [initiative_settings.department.email],
                "from_mail": str(DynamicEmailConfiguration.get_solo().from_email),
            }
            send_email_initiative_broadcast.apply_async(kwargs=mail_content)

        email_builder = EmailBuilder(
            initiative,
            role_broadcast_template_string=EmailString.PREMODERATION_INITIATIVE_CREATED,
        )
        email_sender = EmailSender(email_builder)
        email_sender.send_role_broadcast(UserRole.MODERATOR)

        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    @action(
        methods=["get"], detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def vote(self, request, pk=None):
        user: User = request.user
        user_age = user.age
        user_locality = user.get_locality_for_initiative()
        esia_verified = user.esia_verified
        instance: Initiative = self.get_object()
        settings: InitiativeSettings = InitiativeSettings.load()

        if instance.state != InitiativeState.VOTES_COLLECTION:
            return Response(
                "Инициатива не в состоянии сбора голосов",
                status=status.HTTP_400_BAD_REQUEST,
            )

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
                "Возраст не соответствует условиям",
                status=status.HTTP_400_BAD_REQUEST
            )

        if settings.user_locality_check:
            if user_locality is None:
                return Response(
                    "В учетной записи ЕСИА не указан адрес проживания/регистрации",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not instance.locality.filter(
                    Q(parent=user_locality) |
                    Q(id=user_locality.id) |
                    Q(localities=user_locality)
            ).exists():
                return Response(
                    "Муниципальное образование инициативы не соответствует адресу проживания/регистрации указанному в учетной записи ЕСИА",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if instance.is_voted(user):
            return Response(
                "Вы уже поддержали инициативу",
                status=status.HTTP_400_BAD_REQUEST
            )

        if instance.is_owner(user):
            return Response(
                "Можно поддержать только чужую инициативу",
                status=status.HTTP_400_BAD_REQUEST,
            )

        UserInitiativeApprove.objects.create(
            user=user, initiative=instance, timestamp=timezone.now()
        )
        # Добавляем бонусы из модуля экология
        try:
            if user.ecology.state != UserState.INITIAL and user.is_simple_user:
                EcologyUserService(user).add_bonuses_on_user_approve_initiative(
                    instance
                )
        except Exception:
            pass

        return Response()
