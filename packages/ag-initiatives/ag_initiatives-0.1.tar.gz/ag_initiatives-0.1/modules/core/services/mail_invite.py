import string

from des.models import DynamicEmailConfiguration
from django.core.mail import send_mail
from django.utils.crypto import random
from rest_framework.exceptions import NotFound

from modules.core.models.mail_invite import *


class MailInviteService:
    def send_invite_message(self, mail_invite: MailInvite, host):
        """Отправляет Текст с приглашением на указанный адрес"""

        if mail_invite.patronymic_name is None:
            patronymic_name = '.'
        else:
            patronymic_name = ' ' + mail_invite.patronymic_name + '.'

        from_email = str(DynamicEmailConfiguration.get_solo().from_email)
        to_email = [mail_invite.email]
        subject = f'Приглашение "Активный гражданин"'
        message = f"""
                       Добрый день, {mail_invite.last_name} {mail_invite.first_name}{patronymic_name}\n
                Для подтверждения учётной записи требуется перейти по ссылке и произвести вход в Госулуги.\n
                Ссылка: {host}accept-user-permissions/{mail_invite.slug}\n
                   """

        if mail_invite.comment is not None:
            message += f"Комментарий: {mail_invite.comment}"

        send_mail(subject, message, from_email, to_email, fail_silently=False)

    def get_by_slug(self, slug) -> MailInvite:
        mail_invite_object = MailInvite.objects.filter(slug=slug).first()
        if not mail_invite_object:
            raise NotFound()
        return mail_invite_object

    def set_is_valid_false(self, invite_obj: MailInvite):
        invite_obj.is_valid = False
        invite_obj.save()

    def unique_slug_generator(self) -> str:
        slug = self._create_random_slug()
        while self._is_slug_exists(slug):
            slug = self._create_random_slug()
        return slug

    @staticmethod
    def get_host(request=None):
        host = "http://24ag.ru/"
        if request:
            host = request.get_host()
            if request.is_secure():
                host = f"https://{host}/"
            else:
                host = f"http://{host}/"
        return host

    def update_user_lko_roles(self, user, invite_obj):
        # not_lko_roles = list(filter(lambda role: role not in LKO_ROLES, user.roles))
        if hasattr(user, 'sub_permissions'):
            su = user.sub_permissions
            su.user = None
            su.save()

        new_roles = invite_obj.roles
        user.sub_permission = invite_obj.sub_permission
        user.roles = new_roles
        user.position = invite_obj.sub_permission.position
        user.work_email = invite_obj.email
        user.work_phone = invite_obj.work_phone
        user.sub_phone = invite_obj.phone
        user.sub_permission.sub_phone = invite_obj.phone
        user.save()
        
        invite_obj.sub_permission.user = user
        invite_obj.sub_permission.save()

        if hasattr(invite_obj.sub_permission, 'admin_lko_permissions'):
            invite_obj.sub_permission.admin_lko_permissions.user = user
            user.admin_lko_permissions.save()
        if hasattr(invite_obj.sub_permission, 'operator_permissions'):
            invite_obj.sub_permission.operator_permissions.user = user
            user.operator_permissions.save()

        # raise Exception(user.admin_lko_permissions)

    def _create_random_slug(self) -> str:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(15))

    def _is_slug_exists(self, slug) -> bool:
        return MailInvite.objects.filter(slug=slug).exists()
