from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .initiative import InitiativeOperatorAPI
from modules.core.permissions import IsOperator
from modules.core.models import User
from modules.appeals_pos.api import AppealApi
from modules.api.viewsets import InitiativeCommunicationAPI
from modules.ecology.api import UserProfileAPI as EcologyUserProfileAPI
from modules.voting.api import VoteOperatorAPI
from modules.initiatives.models import InitiativeAcceptingSettings
from modules.map_works.api import WorksOperatorAPI
from modules.plans.api import PlanOperatorAPI


class OperatorInfoAPI(viewsets.ViewSet):
    permission_classes = [IsOperator]

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
        works_count = WorksOperatorAPI.as_view({"get": "count"})(request._request).data["count"]
        plans_count = PlanOperatorAPI.as_view({"get": "count"})(request._request).data["count"]
        votes_count = VoteOperatorAPI.as_view({"get": "count"})(request._request).data["count"]
        opinions_count = user.opinions.all().count()
        initiatives_count = InitiativeOperatorAPI.as_view({"get": "count"})(request._request).data["count"]

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
            ).count() if department else None,
            "messages": {
                "unread": 0,
                "total": None,
            },
        }
        return Response(res)
