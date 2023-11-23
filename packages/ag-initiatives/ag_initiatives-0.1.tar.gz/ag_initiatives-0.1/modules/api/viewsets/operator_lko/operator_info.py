from django.db.models import Q
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.viewsets.operator_lko.initiative import InitiativeOperatorLkoAPI
from modules.api.viewsets.operator_lko.initiative_accepting_settings import (
    InitiativeSettingsOperatorLkoAPI
)
from modules.api.viewsets.operator_lko.map_works import MapWorksOperatorLkoAPI
from modules.api.viewsets.operator_lko.plans import PlanOperatorLkoAPI
from modules.api.viewsets.operator_lko.voting import VotingOperatorLkoAPI
from modules.core.models import RoleInstruction, UserRole
from modules.core.models.permissions import ModulesPermissions
from modules.core.permissions import IsOperator
from modules.core.services.operator_lko import OperatorLkoService
from modules.ecology.exceptions import OrganizerError, PartnerError
from modules.ecology.services import OrganizerService
from modules.ecology.services.partner_service import PartnerService
from modules.feedback.models import Opinion
from modules.voting.models import LocalVotingGroup


class OperatorLkoInfoAPI(viewsets.ViewSet):

    permission_classes = [IsOperator]

    def list(self, request: Request) -> Response:
        user = request.user
        modules_permissions = user.sub_permissions.operator_permissions.modules_permissions

        works_api_cls = MapWorksOperatorLkoAPI if ModulesPermissions.MAP_WORKS in modules_permissions else None
        plans_api_cls = PlanOperatorLkoAPI if ModulesPermissions.PLANS in modules_permissions else None
        voting_api_cls = VotingOperatorLkoAPI if ModulesPermissions.VOTING in modules_permissions else None
        initiatives_api_cls = InitiativeOperatorLkoAPI if ModulesPermissions.INITIATIVES in modules_permissions else None
        initiative_settings_api_cls = (
            InitiativeSettingsOperatorLkoAPI
            if ModulesPermissions.INITIATIVES in modules_permissions else None
        )

        local_voting_groups_count = LocalVotingGroup.objects.all().count()


        works_count = (
            None
            if works_api_cls is None
            else works_api_cls.as_view({"get": "count"})(request._request).data.get("count")
        )

        plans_count = (
            None
            if plans_api_cls is None
            else plans_api_cls.as_view({"get": "count"})(request._request).data.get("count")
        )

        voting_count = (
            None
            if voting_api_cls is None
            else voting_api_cls.as_view({"get": "count"})(request._request).data.get("count")
        )

        initiatives_count = (
            None
            if initiatives_api_cls is None
            else initiatives_api_cls.as_view({"get": "count"})(request._request).data.get("count")
        )

        initiative_settings_count = (
            None
            if initiative_settings_api_cls is None
            else initiative_settings_api_cls.as_view({"get": "count"})(request._request).data.get("count")
        )

        roles_instructions = RoleInstruction.objects.filter(role=UserRole.OPERATOR).first()
        instructions_count = roles_instructions.instructions.all().count() if roles_instructions else 0
        try:
            participation_count = OrganizerService(user).get_users_participation().count()
        except OrganizerError:
            participation_count = 0
        try:
            history_count = PartnerService(user).get_users_purchases().count()
        except PartnerError:
            history_count = 0
        try:
            requests_count = PartnerService(user).get_history().count()
        except PartnerError:
            requests_count = 0

        try:
            service = OperatorLkoService(user=self.request.user, module=ModulesPermissions.APPEALS)
            opinions_count = Opinion.objects.filter(
                Q(locality__in=service.get_allowed_localities()) | Q(locality__isnull=True),
                problematic__in=service.get_allowed_categories(),
            ).distinct().count()
        except PartnerError:
            opinions_count = 0

        return Response({
            "modules_permission": modules_permissions,
            "counts": {
                "works": works_count,
                "plans": plans_count,
                "votes": voting_count,
                "instructions": instructions_count,
                "local_voting_groups": local_voting_groups_count,
                "initiatives": initiatives_count,
                "initiative_settings": initiative_settings_count,
                "opinions_count": opinions_count,
                "history": history_count,
                "participation": participation_count,
                "requests": requests_count,
            }
        })
