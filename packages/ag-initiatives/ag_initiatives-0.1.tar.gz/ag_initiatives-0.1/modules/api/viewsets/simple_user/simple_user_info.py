from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .initiative import InitiativeSimpleUserAPI
from modules.core.models import User
from modules.appeals_pos.api import AppealApi
from modules.api.viewsets import InitiativeCommunicationAPI
from modules.ecology.api import UserProfileAPI as EcologyUserProfileAPI
from modules.initiatives.models import (
    InitiativeAcceptingSettings,
    InitiativeOperatorCommunication,
)


class SimpleUserInfoAPI(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        user: User = request.user
        department = getattr(user, "department", None)

        appeals_count = AppealApi.as_view({"get": "count"})(request._request).data[
            "count"
        ]

        notifications_count = (
                len(AppealApi.as_view({"get": "my_pos_notifications"})(request._request).data)
                + len(
            InitiativeCommunicationAPI.as_view({"get": "list"})(
                request._request
            ).data
        )
                + len(
            EcologyUserProfileAPI.as_view({"get": "notifications"})(
                request._request
            ).data
        )
        )

        works_count = 0
        plans_count = 0
        votes_count = 0
        opinions_count = user.opinions.all().count()
        initiatives_count = InitiativeSimpleUserAPI.as_view({"get": "count"})(request._request).data["count"]

        res = {
            "notifications_count": notifications_count,
            "appeals_count": appeals_count,
            "initiatives_count": initiatives_count,
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
            },
        }
        return Response(res)
