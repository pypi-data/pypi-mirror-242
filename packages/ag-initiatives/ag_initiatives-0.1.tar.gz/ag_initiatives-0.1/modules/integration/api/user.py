import requests
from django.db import transaction
from django.db.models import Prefetch, Q, When, Case, BooleanField, OuterRef, Subquery
from requests.sessions import InvalidSchema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from modules.core.authentication_classes import ExternalSystemTokenAuthentication
from modules.core.models import User
from modules.core.models.category_citizen import CategoryCitizen
from modules.ecology.models import (
    Notification,
    NotificationType,
    UserBalanceOperationType,
)
from modules.ecology.models.user_profile import UserState
from modules.integration.api.event import EventForIntegrationByUserApi
from modules.integration.api.goodsnservicesitem import IntegrationGoodsNServicesItemAPI
from modules.integration.api.initiative import InitiativeAPI
from modules.integration.api.serializers.user import (
    NotificationSerializer,
    UserSerializer, UserUpdateSerializer, UserECardGetSerializer,
)
from modules.integration.api.serializers.user_balance_operation import (
    UserBalanceOperationSerializer,
)
from modules.integration.api.serializers.user_synchronization import (
    UserSynchronizationSerializer,
)
from modules.integration.api.voting import VoteAPI
from modules.integration.models.user_synchronization import UserSynchronization
from modules.integration.permissions import (
    CanGetOperationHistoryOfUser,
    CanGetUserBalance,
    CanSinchronizeUser,
    CanTransmitBonuses,
)
from modules.voting.models import UserVote


class UserAPI(GenericViewSet):
    serializer_class = UserSerializer
    authentication_classes = [ExternalSystemTokenAuthentication]
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def get_serializer_class(self):
        if self.action == "create":
            return UserSynchronizationSerializer
        if self.action == "add_balance_operation":
            return UserBalanceOperationSerializer
        if self.action == "list":
            return UserECardGetSerializer
        return self.serializer_class

    def get_queryset(self):
        return User.objects.filter(is_archive=False).select_related().prefetch_related(
            "categories",
            Prefetch(
                "notifications",
                queryset=Notification.objects.select_related(
                    "user_balance_operation",
                ),
            ),
        )

    def get_permissions(self):
        if self.action == "operations":
            return [CanGetOperationHistoryOfUser()]
        if self.action == "balance":
            return [CanGetUserBalance()]
        if self.action == "add_balance_operation":
            return [CanTransmitBonuses()]
        return [CanSinchronizeUser()]

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data.get("id"))
        except User.DoesNotExist:
            return Response(
                "Пользователь с таким ID не найден.", status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(
            data={**request.data, "external_system": request.external_system.pk}
        )
        if serializer.is_valid():
            instance: UserSynchronization = serializer.save()
            user: User = instance.user
        serializer_data = serializer.data
        serializer_data.pop("external_system", None)
        # Send request for external system for check user.

        try:
            headers = {"Authorization": f"Token {request.external_system.system_token}"}
            snils = f'snils={user.snils}&' if user.snils else ''
            phone = f'phone={user.phone}&' if user.phone else ''
            response = requests.get(
                f"{request.external_system.url}/api/e-card/users/?{snils}{phone}",
                headers=headers,
                verify=False,
            )
        except InvalidSchema:
            return Response(
                "Для вашей системы неверно указан URL в административном интерфейсе."
            )
        if 200 > response.status_code >= 300:
            return Response(serializer_data, status=status.HTTP_200_OK)
        try:
            data = response.json()
            if len(data) <= 0:
                return Response(f"Во внешней системе не наёден пользователь.")
            for category in response.json()[0].get("categories", []):
                if not user.categories.filter(name__icontains=category):
                    category_instance, _ = CategoryCitizen.objects.get_or_create(name=category)
                    user.categories.add(category_instance)
        except LookupError:
            return Response(
                f"Неожиданное тело ответа: {response.json()} по апи /api/e-card/users/ внешней системы."
            )
        return Response(serializer_data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        try:
            query = Q()
            if "snils" in request.query_params:
                snils = str(request.query_params.get("snils"))
                formatted_snils = f"{snils[0:3]}-{snils[3:6]}-{snils[6:9]} {snils[9:11]}"
                query |= (Q(is_active=True) & (Q(snils=formatted_snils) | Q(snils=snils)))
            if "phone" in request.query_params:
                phone = "+" + str(request.query_params.get("phone")).strip()
                analog_phone = "8" + phone[2:]
                query |= (Q(is_active=True) & (Q(phone=phone) | Q(phone=analog_phone)))
            if not query:
                return Response("Не указаны фильтры", status=500)
            queryset = self.get_queryset().filter(query)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except (IndexError, KeyError):
            return Response(status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    @action(detail=True, methods=['post'], url_path="")
    def create_with_id(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                "Пользователь с таким ID не найден.", status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserUpdateSerializer(
            instance=user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True)
    def operations(self, request: Request, pk=None, *args, **kwargs):
        operation_id = request.query_params.get("last_operation")
        user = User.objects.get(id=pk)
        balance = user.ecology.balance
        operations = Notification.objects.filter(
            user=user, id__gte=operation_id
        ).select_related("user_balance_operation")
        operations_data = NotificationSerializer(operations, many=True).data

        return Response(
            {
                "balance": balance,
                "operations": operations_data,
            }
        )

    @action(detail=True)
    def balance(self, request: Request, pk=None, *args, **kwargs):
        try:
            balance = User.objects.get(pk=pk).ecology.balance
            return Response({"id": int(pk), "balance": balance})

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic()
    @action(detail=True, methods=["post"], url_path="add-balance-operation")
    def add_balance_operation(self, request: Request, pk=None, *args, **kwargs):
        user: User = User.objects.filter(pk=pk).first()
        synchronized_user = UserSynchronization.objects.filter(user_id=user.pk).exists()

        if not user or not synchronized_user:
            return Response(
                "Неверно указан идентификатор пользователя или он не синхронизирован.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_balance_operation = serializer.save(user_id=int(pk))

        amount, date, type = (
            request.data.get("amount"),
            request.data.get("date"),
            request.data.get("type"),
        )
        amount = int(amount)

        if type == "INCOME":
            user.ecology_profile.earned_bonuses += amount
            user.ecology_profile.balance += amount
            user.ecology_profile.state = UserState.PARTICIPATE
            user.ecology_profile.save(
                update_fields=["balance", "state", "earned_bonuses"]
            )

        if type == "EXPENSE":
            user.ecology_profile.state = UserState.PARTICIPATE
            if user.ecology_profile.balance - amount < 0:
                user.ecology_profile.save(update_fields=["state"])
                return Response(
                    "Недостаточно средств на выполнение операции.",
                    status=status.HTTP_204_NO_CONTENT,
                )

            user.ecology_profile.balance -= amount
            user.ecology_profile.save(update_fields=["balance", "state"])

        notification_type = (
            NotificationType.EXTERNAL_INCREASE
            if user_balance_operation.type == UserBalanceOperationType.INCOME
            else NotificationType.EXTERNAL_REDUCTION
        )
        Notification.objects.create(
            user_id=user_balance_operation.user_id,
            timestamp=user_balance_operation.timestamp,
            text=f"{NotificationType.RESOLVER[notification_type]} на {user_balance_operation.amount}",
            type=notification_type,
            user_balance_operation=user_balance_operation,
            target=user_balance_operation.target,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="vote")
    def vote(self, request: Request, pk, *args, **kwargs):
        view = VoteAPI()
        request.user = User.objects.get(pk=pk)
        view.request = request
        view.format_kwarg = None
        view.action = "vote"

        user_votes_subquery = UserVote.objects.filter(
            vote=OuterRef('pk'), user=request.user
        ).values('vote__id')
        qs = view.get_queryset().annotate(
            user_has_voted=Case(
                When(id__in=Subquery(user_votes_subquery), then=True),
                default=False,
                output_field=BooleanField()
            )
        ).order_by("user_has_voted", "-start_date")
        if "user_has_voted" in request.GET:
            qs = qs.filter(user_has_voted=request.GET["user_has_voted"] == "true")
        view.get_queryset = lambda: qs
        return view.list(request)

    @action(detail=True, methods=["get"], url_path="initiative")
    def initiative(self, request: Request, pk, *args, **kwargs):
        view = InitiativeAPI()
        request.user = User.objects.get(pk=pk)
        view.request = request
        view.format_kwarg = None
        view.action = "initiative"

        qs = view.get_queryset().annotate(
            user_has_initiative=Case(
                When(user_initiative_approve__user=request.user, then=True),
                default=False,
                output_field=BooleanField()
            ),
            user_created_initiative=Case(
                When(user=request.user, then=True),
                default=False,
                output_field=BooleanField()
            )
        ).order_by("user_has_initiative", "user_created_initiative", "-votes_collection_begin_date")
        if "user_has_initiative" in request.GET:
            qs = qs.filter(user_has_initiative=request.GET["user_has_initiative"] == "true")
        if "user_created_initiative" in request.GET:
            qs = qs.filter(user_created_initiative=request.GET["user_created_initiative"] == "true")
        view.get_queryset = lambda: qs

        return view.list(request)

    @action(detail=True, methods=["get"], url_path="offers")
    def offers(self, request: Request, pk, *args, **kwargs):
        view = EventForIntegrationByUserApi()
        request.user = User.objects.get(pk=pk)
        view.request = request
        view.format_kwarg = None
        view.action = "offers"

        qs = view.get_queryset().annotate(
            user_has_offer=Case(
                When(participation_user_event_event__participant=request.user, then=True),
                default=False,
                output_field=BooleanField()
            ),
        ).order_by("user_has_offer", "-start_date")
        if "user_has_offer" in request.GET:
            qs = qs.filter(user_has_offer=request.GET["user_has_offer"] == "true")
        view.get_queryset = lambda: qs

        return view.list(request)

    @action(detail=True, methods=["get"], url_path="rewards")
    def rewards(self, request: Request, pk, *args, **kwargs):
        view = IntegrationGoodsNServicesItemAPI()
        request.user = User.objects.get(pk=pk)
        view.request = request
        view.format_kwarg = None
        view.action = "rewards"

        qs = view.get_queryset().annotate(
            user_has_reward=Case(
                When(purchases__user=request.user, then=True),
                default=False,
                output_field=BooleanField()
            ),
        ).order_by("user_has_reward", "-start_date")
        if "user_has_reward" in request.GET:
            qs = qs.filter(user_has_reward=request.GET["user_has_reward"] == "true")
        view.get_queryset = lambda: qs

        return view.list(request)
