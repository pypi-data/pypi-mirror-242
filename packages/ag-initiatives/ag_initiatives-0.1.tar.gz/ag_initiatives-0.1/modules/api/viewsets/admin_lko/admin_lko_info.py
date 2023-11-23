from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from modules.core.models import User, RoleInstruction, UserRole
from modules.core.permissions import IsAdminLKO
from modules.core.services import AdminLkoService
from modules.voting.models import LocalVotingGroup


class AdminLkoInfoAPI(viewsets.ViewSet):

    permission_classes = [IsAdminLKO]

    def get_admin_lko_service(self, user: User) -> AdminLkoService:
        return AdminLkoService(user)

    def list(self, request: Request) -> Response:
        service = self.get_admin_lko_service(request.user)

        departments_count = len(list(service.get_allowed_departments()))
        users_count = service.get_allowed_users().count()
        local_voting_groups = LocalVotingGroup.objects.all().count()
        roles_instructions = RoleInstruction.objects.filter(role=UserRole.ADMIN_LKO).first()
        instructions_count = roles_instructions.instructions.all().count() if roles_instructions else 0

        return Response({
            "counts": {
                "departments": departments_count,
                "users": users_count,
                "local_voting_groups": local_voting_groups,
                "instructions": instructions_count
            }
        })
