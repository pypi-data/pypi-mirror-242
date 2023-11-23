from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.core.models import User, ActiveCitizenModule
from modules.core.models.active_citizen_module import ActiveCitizenModuleEnum
from modules.core.permissions import IsUser
from modules.ecology.api.filters import EventFilter
from modules.ecology.api.filters.participation import ParticipationFilter
from modules.ecology.api.filters.purchase import UserPurchaseFilter
from modules.ecology.api.serializers import (
    UserEventListSerializer,
    UserEventDetailsSerializer,
    NotificationSerializer,
    ParticipationSerializer,
    UserBalanceOperationSerializer,
)
from modules.ecology.api.serializers import SurveySerializer
from modules.ecology.api.serializers.participation import (
    ParticipationUserListSerializer,
)
from modules.ecology.api.serializers.user_purchase import UserPurchaseSerializer
from modules.ecology.exceptions import UserError, BalanceOperationError
from modules.ecology.models import (
    Event,
    UserState,
    UserBalanceOperation,
    Settings,
    UserBalanceOperationType,
    Notification,
    NotificationType,
    EcologyLevel,
    Survey,
    SurveyQuestion,
    UserSurvey,
    GoodsNServicesItem,
    UserPurchase,
    ParticipationUserEvent,
)
from django_filters import rest_framework as filters

from modules.ecology.pagination import DefaultPagination
from modules.ecology.services import QRGenerator
from modules.ecology.services.user_service import UserService
from modules.ecology.tasks import send_email_on_ecology_participation


class UserParticipationAPI(viewsets.ViewSet):

    permission_classes = [IsUser]
    filter_class = ParticipationFilter

    def list(self, request):
        user: User = request.user
        try:
            queryset = UserService(user).get_participations()
        except UserError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        filtered_queryset = self.filter_class(
            data=request.query_params, queryset=queryset
        ).qs

        paginator = DefaultPagination()
        page = paginator.paginate_queryset(filtered_queryset, request=request)
        response = paginator.get_paginated_response(
            ParticipationUserListSerializer(page, many=True).data
        )
        return response

    def create(self, request):
        user: User = request.user
        event_id = request.data.get("event_id", None)
        if not event_id:
            return Response(
                "Не указан id предложения", status=status.HTTP_400_BAD_REQUEST
            )

        event: Event = Event.objects.filter(pk=event_id).first()
        if not event:
            return Response(
                "Предложение не найдено", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            participation_user_event = UserService(user).event_participate(event)
        except UserError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        host = QRGenerator.get_host(request)
        qr_data = f"{host}organizer/qr-scan/{participation_user_event.pk}"
        svg_qrcode = QRGenerator(qr_data).svg
        return HttpResponse(svg_qrcode, content_type="image/svg+xml")

    @action(methods=["get"], detail=True, url_path="get-qr")
    def qet_qr(self, request, pk):
        participation = ParticipationUserEvent.objects.filter(id=pk).first()

        if not participation:
            return Response(
                "Участие в предложении не найдено", status=status.HTTP_400_BAD_REQUEST
            )

        host = QRGenerator.get_host(request)
        qr_data = f"{host}organizer/qr-scan/{participation.pk}"
        svg_qrcode = QRGenerator(qr_data).svg
        return HttpResponse(svg_qrcode, content_type="image/svg+xml")


class UserPurchaseAPI(viewsets.ViewSet):

    permission_classes = [IsUser]
    filter_class = UserPurchaseFilter

    def list(self, request):
        user: User = request.user
        try:
            queryset = UserService(user).get_purchases()
        except UserError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        filtered_queryset = self.filter_class(
            data=request.query_params, queryset=queryset
        ).qs

        paginator = DefaultPagination()
        page = paginator.paginate_queryset(filtered_queryset, request=request)
        response = paginator.get_paginated_response(
            UserPurchaseSerializer(page, many=True).data
        )
        return response

    def create(self, request):
        user: User = request.user
        item_id = request.data.get("item_id")
        item: GoodsNServicesItem = GoodsNServicesItem.objects.filter(pk=item_id).first()
        if not item:
            return Response("Данного поощрения не существует")

        try:
            purchase = UserService(user).purchase(item)
        except (UserError, BalanceOperationError) as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserPurchaseSerializer(purchase).data)

    @action(methods=["get"], detail=True, url_path="return", url_name="return")
    def purchase_return(self, request, pk):
        user: User = request.user
        purchase: UserPurchase = UserPurchase.objects.filter(pk=pk).first()
        if not purchase:
            return Response("Покупка не найдена", status=status.HTTP_400_BAD_REQUEST)

        try:
            purchase = UserService(user).return_purchase(purchase)
        except (UserError, BalanceOperationError) as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserPurchaseSerializer(purchase).data)


class UserProfileAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.none()
    serializer_class = UserEventListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter
    pagination_class = LimitOffsetPagination
    permission_classes = [IsUser]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserEventDetailsSerializer
        return super().get_serializer_class()

    @transaction.atomic
    @action(methods=["get"], detail=False)
    def participate(self, request):
        user: User = request.user

        if user.ecology.state != UserState.INITIAL:
            return Response(
                "Пользователь уже участвует", status=status.HTTP_400_BAD_REQUEST
            )

        settings: Settings = Settings.load()

        now_time = timezone.now()

        user.ecology_profile.earned_bonuses += settings.participation_reward
        user.ecology_profile.balance += settings.participation_reward
        user.ecology_profile.state = UserState.PARTICIPATE
        user.ecology_profile.save(update_fields=["balance", "state", "earned_bonuses"])

        user_balance_operation = UserBalanceOperation.objects.create(
            user=user,
            timestamp=now_time,
            type=UserBalanceOperationType.INCOME,
            amount=settings.participation_reward,
            reason="PARTICIPATE",  # todo сделать enum?
        )

        Notification.objects.create(
            user=user,
            timestamp=now_time,
            text=f"Вам начислено {settings.participation_reward} приветственных бонусов за участие в проекте.",
            type=NotificationType.PARTICIPATE,
            user_balance_operation=user_balance_operation,
        )

        response_data = {"reward": settings.participation_reward}

        send_email_on_ecology_participation.delay(
            to=[user.email], reward=settings.participation_reward
        )

        return Response(response_data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def notifications(self, request):
        user: User = request.user
        ecology_stimulation_module = ActiveCitizenModule.objects.filter(
            name=ActiveCitizenModuleEnum.ECOLOGY_STIMULATION).first()
        notifocations = Notification.objects.filter(user=user).order_by("-timestamp")
        if not ecology_stimulation_module.is_worked:
            notifocations = notifocations.exclude(type__in=(
                NotificationType.GOODSNSERVICES_PURCHASE,
                NotificationType.RETURN_GOODSNSERVICES_PURCHASE
            ))
        ecology_offers_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.ECOLOGY_OFFERS).first()
        if not ecology_offers_module.is_worked:
            notifocations = notifocations.exclude(type__in=(
                NotificationType.DECLINE_EVENT_PARTICIPATION,
                NotificationType.EVENT_PARTICIPATION
            ))

        return Response(NotificationSerializer(notifocations, many=True).data)

    @action(methods=["get"], detail=False)
    def survey_suspend(self, request):
        user: User = request.user

        if user.ecology.state != UserState.PARTICIPATE:
            return Response(
                "Пользователь не участвует в проекте или анкета уже заполнена",
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.ecology_profile.state = UserState.SURVEY_SUSPEND
        user.ecology_profile.save(update_fields=["state"])

        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=["post"], detail=False)
    def survey(self, request):
        user: User = request.user

        if user.ecology.state in [UserState.SURVEY_COMPLETED]:
            return Response(
                "Анкета уже заполнена",
                status=status.HTTP_400_BAD_REQUEST,
            )

        survey: Survey
        try:
            survey = Survey.objects.get(pk=request.data.pop("id", None))
        except:
            return Response(
                "Некорректный анкеты id", status=status.HTTP_400_BAD_REQUEST
            )

        now_time = timezone.now()

        try:
            for question_id in request.data.keys():
                if type(request.data[question_id]) is list:
                    for answer_id in request.data[question_id]:
                        question = survey.questions.get(pk=question_id)
                        answer = question.answers.get(pk=answer_id)
                        UserSurvey.objects.create(
                            user=user,
                            survey=survey,
                            question=question,
                            answer=answer,
                            timestamp=now_time,
                        )
                else:
                    answer_id = request.data[question_id]
                    question = survey.questions.get(pk=question_id)
                    answer = question.answers.get(pk=answer_id)
                    UserSurvey.objects.create(
                        user=user,
                        survey=survey,
                        question=question,
                        answer=answer,
                        timestamp=now_time,
                    )

        except Exception as e:
            raise ValidationError("Некорректные данные", status.HTTP_400_BAD_REQUEST)

        settings: Settings = Settings.load()

        user.ecology_profile.earned_bonuses += settings.survey_reward
        user.ecology_profile.balance += settings.survey_reward
        user.ecology_profile.state = UserState.SURVEY_COMPLETED
        user.ecology_profile.save(update_fields=["balance", "state", "earned_bonuses"])

        user_balance_operation = UserBalanceOperation.objects.create(
            user=user,
            timestamp=now_time,
            type=UserBalanceOperationType.INCOME,
            amount=settings.survey_reward,
            reason="SURVEY_COMPLETED",  # todo сделать enum?
        )

        Notification.objects.create(
            user=user,
            timestamp=now_time,
            text=f"Вам начислено {settings.survey_reward} бонусов за заполнение анкеты.",
            type=NotificationType.SURVEY_COMPLETED,
            user_balance_operation=user_balance_operation,
        )

        response_data = {
            "reward": settings.survey_reward,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=["get"], detail=False, url_path="get-survey")
    def get_survey(self, request):
        survey = Survey.objects.order_by("-timestamp_add").first()
        return Response(SurveySerializer(survey).data, status=status.HTTP_200_OK)
