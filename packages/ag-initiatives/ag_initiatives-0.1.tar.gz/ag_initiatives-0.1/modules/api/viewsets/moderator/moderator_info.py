from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from modules.appeals.models import Appeal, AppealState
from .initiative import InitiativeModeratorAPI
from modules.core.permissions import IsModerator
from modules.core.models import User
from modules.appeals_pos.api import AppealApi
from modules.api.viewsets import InitiativeCommunicationAPI
from modules.ecology.api import UserProfileAPI as EcologyUserProfileAPI
from modules.plans.api import PlanCommentModeratorAPI
from modules.voting.api import VoteModeratorAPI
from modules.initiatives.models import InitiativeAcceptingSettings


class ModeratorInfoAPI(viewsets.ViewSet):
    permission_classes = [IsModerator]

    def list(self, request: Request) -> Response:
        user: User = request.user
        department = getattr(user, "department", None)

        appeals_count = Appeal.objects.filter(
                state=AppealState.MODERATION,
            ).count()

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
        plans_count = PlanCommentModeratorAPI.as_view({"get": "count"})(request._request).data["count"]
        votes_count = VoteModeratorAPI.as_view({"get": "count"})(request._request).data["count"]
        opinions_count = user.opinions.all().count()
        initiatives_count = InitiativeModeratorAPI.as_view({"get": "count"})(request._request).data["count"]

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
                "total": None,
            },
        }
        return Response(res)
