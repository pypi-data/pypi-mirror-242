from django.db import transaction, IntegrityError

from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from modules.core.models import MailInvite, User, SubPermissions
from modules.core.services import MailInviteService
from modules.api.serializers import MailInviteSerializer


class MailInviteAPI(CreateModelMixin,
                    GenericViewSet):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MailInviteSerializer
    queryset = MailInvite.objects.all()
    service = MailInviteService()

    "Если slug не был передан, то генерирует уникальный"
    @transaction.atomic
    def save_data_and_send_mail(self, request, sub_permission_pk: int):
        data: dict = request.data
        sub_permissions_data: dict = data.pop("sub_permissions", None)
        data.update(sub_permissions_data)
        data.setdefault("sub_permission", sub_permission_pk)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mail_invite = serializer.save()
        host = self.service.get_host(request)
        self.service.send_invite_message(mail_invite, host)


    @transaction.atomic
    @action(methods=["post"], detail=True, url_path="accept-user-permissions")
    def accept_user_permissions(self, request: Request, pk: MailInvite.slug):
        invite_obj: MailInvite = self.service.get_by_slug(pk)
        if invite_obj.is_valid:

            user: User = request.user
            self.service.update_user_lko_roles(user, invite_obj)
            self.service.set_is_valid_false(invite_obj)

        else:
            raise ValidationError("Данный слаг недействителен.")
        return Response()
