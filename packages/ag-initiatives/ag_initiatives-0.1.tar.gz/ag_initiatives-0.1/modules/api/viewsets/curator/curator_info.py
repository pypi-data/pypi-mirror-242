from typing import List

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.viewsets.curator.department import DepartmentsCuratorAPI
from modules.api.viewsets.curator.initiative import CuratorInitiativeApi
from modules.api.viewsets.curator.initiative_accepting_settings import (
    CuratorInitiativeSettingsAPI
)
from modules.api.viewsets.curator.map_works import CuratorMapWorksApi
from modules.api.viewsets.curator.plans import CuratorPlansApi
from modules.api.viewsets.curator.user_manager import UserManagerApi
from modules.api.viewsets.curator.voting import CuratorVotingApi
from modules.core.models import User, RoleInstruction, UserRole
from modules.core.models.permissions import ModulesPermissions
from modules.core.permissions import IsOperator


class CuratorInfoAPI(viewsets.ViewSet):

    permission_classes = [IsOperator]

    def get_modules_permissions(self, user: User) -> List[str]:
        modules_permissions = set()
        if not hasattr(user, 'sub_permissions'):
            return []
        if not hasattr(user.sub_permissions, 'curator_permissions'):
            return []

        curator_permissions = user.sub_permissions.curator_permissions.all()
        for curator_permission in curator_permissions:
            modules_permissions = modules_permissions | set(curator_permission.modules_permissions)

        return list(modules_permissions)

    def list(self, request: Request) -> Response:

        modules_permissions = self.get_modules_permissions(request.user)

        works_api_cls = CuratorMapWorksApi if ModulesPermissions.MAP_WORKS in modules_permissions else None
        plans_api_cls = CuratorPlansApi if ModulesPermissions.PLANS in modules_permissions else None
        voting_api_cls = CuratorVotingApi if ModulesPermissions.VOTING in modules_permissions else None
        initiatives_api_cls = CuratorInitiativeApi if ModulesPermissions.INITIATIVES in modules_permissions else None
        initiative_settings_api_cls = (
            CuratorInitiativeSettingsAPI
            if ModulesPermissions.INITIATIVES in modules_permissions else None
        )

        users_api_cls = UserManagerApi
        department_api_cls = DepartmentsCuratorAPI

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
            else initiative_settings_api_cls.as_view(
                {"get": "count"})(request._request).data.get("count")
        )

        users_count = users_api_cls.as_view({"get": "count"})(request._request).data.get("count")

        roles_instructions = RoleInstruction.objects.filter(role=UserRole.OPERATOR).first()
        instructions_count = roles_instructions.instructions.all().count() if roles_instructions else 0

        departments_count = department_api_cls.as_view({"get": "count"})(request._request).data.get("count")

        return Response({
            "modules_permissions": modules_permissions,
            "counts": {
                "works": works_count,
                "plans": plans_count,
                "votes": voting_count,
                "instructions": instructions_count,
                "users": users_count,
                "departments": departments_count,
                "initiatives": initiatives_count,
                "initiative_settings": initiative_settings_count,
            }
        })
