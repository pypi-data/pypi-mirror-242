from rest_framework import serializers

from modules.core.models import MailInvite, UserRole
from modules.core.services import MailInviteService


class MailInviteSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(default=MailInviteService().unique_slug_generator)
    roles = serializers.MultipleChoiceField(choices=list(UserRole.CHOICES))

    class Meta:
        model = MailInvite
        exclude = [
            "operator_permissions",
            "admin_lko_permissions",
        ]
