from datetime import datetime

from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from modules.api.serializers import UserShortSerializer, UserArchivingSerializer
from modules.api.viewsets import InitiativeCommunicationAPI
from modules.appeals.api import AppealModeratorAPI, AppealOperatorAPI, AppealUserAPI
from modules.appeals.api.serializers import AppealOwnerCommunicationsUserSerializer
from modules.appeals.models import (
    AppealOwnerCommunications,
    AppealOwnerCommunicationType,
)
from modules.appeals_pos.api import AppealApi
from modules.core.admin.user import remove_esia_raw_data
from modules.core.mixins.user_track_admin import TrackUserApiMixin
from modules.core.models import User
from modules.core.models.active_citizen_module import ActiveCitizenModuleEnum, ActiveCitizenModule
from modules.initiatives.models import (
    InitiativeAcceptingSettings,
    InitiativeOperatorCommunication,
)

from modules.ecology.api import UserProfileAPI as EcologyUserProfileAPI
from modules.map_works.api import WorksOperatorAPI
from modules.plans.api import PlanOperatorAPI, PlanModeratorAPI, PlanCommentModeratorAPI
from modules.voting.api import VoteModeratorAPI, VoteOperatorAPI
from modules.core.models.user import UserRole
from modules.feedback.models import Opinion


class UserProfileAPI(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response(UserShortSerializer(request.user).data)

    @action(detail=False, methods=["delete"])
    def delete(self, request):
        user = request.user
        esia = request.query_params.get("esia", None)
        snils = user.snils
        if snils != esia:
            return Response({"message": "Неверный СНИЛС"}, status=400)
        if user.deletion_date is not None:
            return Response({"message": "Удаление учётной записи уже было запрошено"}, status=400)
        time_zone = timezone.get_current_timezone()
        user.deletion_date = datetime.now().astimezone(time_zone)
        user.save()
        return Response({"message": "Удаление учётной записи успешно запрошено"})

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_operator:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user: User
        try:
            user = User.objects.get(pk=kwargs.get("pk", None))
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(UserShortSerializer(user).data)

    @action(methods=["get"], detail=False)
    def toggle_email_notifications(self, request):
        user: User = request.user
        user.email_initiative_notification = not user.email_initiative_notification
        user.save(update_fields=["email_initiative_notification"])
        TrackUserApiMixin.create(request, user, None, True)
        return Response(UserShortSerializer(user).data)

    @action(methods=["get"], detail=False)
    def toggle_appeals_email_notifications(self, request):
        user: User = request.user
        user.email_appeals_notification = not user.email_appeals_notification
        user.save(update_fields=["email_appeals_notification"])
        TrackUserApiMixin.create(request, user, None, True)
        return Response(UserShortSerializer(user).data)

    @action(methods=["get"], detail=False)
    def objects_counts(self, request):
        user: User = request.user
        department = getattr(user, "department", None)

        appeals_count = AppealApi.as_view({"get": "count"})(request._request).data[
            "count"
        ]

        appeal_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.APPEALS_POS).first()
        initiative_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.INITIATIVES).first()
        ecology_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.ECOLOGY).first()
        appeal_notification_count = len(
            AppealUserAPI.as_view({"get": "notifications"})(request._request).data
        ) if appeal_module and appeal_module.is_worked else 0
        initiative_notification_count = len(
            InitiativeCommunicationAPI.as_view({"get": "list"})(request._request).data
        ) if initiative_module and initiative_module.is_worked else 0
        ecology_notification_count = len(
            EcologyUserProfileAPI.as_view({"get": "notifications"})(
                request._request
            ).data
        ) if ecology_module and ecology_module.is_worked else 0
        appeal_pos_notification_count = len(
            AppealApi.as_view(
                {"get": "my_pos_notifications"}
            )(request._request).data) if appeal_module and appeal_module.is_worked else 0
        appeal_owner_communication = AppealOwnerCommunications.objects.filter(
                    appeal__create_by_operator=False,
                    type=AppealOwnerCommunicationType.REQUEST,
                    appeal__user=request.user,
                ).count()
        notifications_count = (appeal_pos_notification_count + appeal_owner_communication +
                               appeal_notification_count + initiative_notification_count + ecology_notification_count)

        works_api_cls = None
        if request.user.is_operator:
            works_api_cls = WorksOperatorAPI

        works_count = (
            0
            if works_api_cls is None
            else works_api_cls.as_view({"get": "count"})(request._request).data["count"]
        )

        plans_api_cls = None
        if request.user.is_operator:
            plans_api_cls = PlanOperatorAPI
        if request.user.is_moderator:
            plans_api_cls = PlanCommentModeratorAPI

        plans_count = (
            0
            if plans_api_cls is None
            else plans_api_cls.as_view({"get": "count"})(request._request).data["count"]
        )

        votes_api_cls = None
        if request.user.is_operator:
            votes_api_cls = VoteOperatorAPI
        if request.user.is_moderator:
            votes_api_cls = VoteModeratorAPI

        votes_count = (
            0
            if votes_api_cls is None
            else votes_api_cls.as_view({"get": "count"})(request._request).data["count"]
        )
        opinions_count = user.opinions.all().count()

        res = {
            "notifications_count": notifications_count,
            "appeals_count": appeals_count,
            "initiatives_count": user.initiatives_for_count,
            "works_count": works_count,
            "opinions_count": opinions_count,
            "plans_count": plans_count,
            "votes_count": votes_count,
            "settings_count": InitiativeAcceptingSettings.objects.filter(
                department=department
            ).count()
            if department
            else None,
            "messages": {
                "unread": 0,
                "total": InitiativeOperatorCommunication.objects.filter(
                    Q(initiative__in=user.initiatives_for_actions) & ~Q(user=user)
                ).count()
                if user.is_simple_user
                else None,
            },
        }
        return Response(res)

    @action(methods=["get"], detail=False, url_path="notification-feed")
    def notification_feed(self, request):
        """
        todo Требуется рефакторинг этой функции
        :param request:
        :return:
        """

        if not request.user.is_simple_user and request.user.is_archive:
            return Response([])

        initiatives_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.INITIATIVES).first()
        ecology_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.ECOLOGY).first()
        appeal_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.APPEALS_POS).first()
        page_num = int(request.GET.get("page_num", "0"))
        page_size = 8  # same as InitiativeCommunicationPagination.page_size

        res = []
        if appeal_module and appeal_module.is_worked:
            for _appeal_owner_communication in AppealOwnerCommunicationsUserSerializer(
                    AppealOwnerCommunications.objects.filter(
                        appeal__create_by_operator=False,
                        type=AppealOwnerCommunicationType.REQUEST,
                        appeal__user=request.user,
                    ),
                    many=True,
            ).data:
                res.append(
                    {
                        "timestamp": _appeal_owner_communication.get("timestamp", None),
                        "type": "appeal_owner_communication",
                        "data": _appeal_owner_communication,
                        "user_role_name": "Модератор",
                    }
                )

            for _appeal_notification in AppealUserAPI.as_view({"get": "notifications"})(
                    request._request
            ).data:
                res.append(
                    {
                        "timestamp": _appeal_notification.get("timestamp", None),
                        "type": "appeal",
                        "data": _appeal_notification,
                    }
                )

            for _appeal_pos_notification in AppealApi.as_view(
                    {"get": "my_pos_notifications"}
            )(request._request).data:
                res.append(
                    {
                        "timestamp": _appeal_pos_notification.get("created_at", None),
                        "type": "appeal_pos",
                        "data": _appeal_pos_notification,
                    }
                )

        if initiatives_module and initiatives_module.is_worked:
            for _initiative_notification in InitiativeCommunicationAPI.as_view(
                    {"get": "list"}
            )(request._request).data:
                res.append(
                    {
                        "timestamp": _initiative_notification.get("timestamp", None),
                        "type": "initiative",
                        "data": _initiative_notification,
                    }
                )

        if ecology_module and ecology_module.is_worked:
            for _ecology_notification in EcologyUserProfileAPI.as_view(
                    {"get": "notifications"}
            )(request._request).data:
                res.append(
                    {
                        "timestamp": _ecology_notification.get("timestamp", None),
                        "type": "ecology",
                        "data": _ecology_notification,
                    }
                )

        res.sort(key=lambda val: val["timestamp"], reverse=True)

        offset = page_num * page_size

        def clamp(val, min_value, max_value):
            return max(min(val, max_value), min_value)

        f = clamp(offset, 0, len(res))
        t = clamp(offset + page_size, 0, len(res))

        return Response(
            {
                "count": len(res),
                "results": res[f:t],
            }
        )


class UserArchivingAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserArchivingSerializer
    permission_classes = [IsAuthenticated]
