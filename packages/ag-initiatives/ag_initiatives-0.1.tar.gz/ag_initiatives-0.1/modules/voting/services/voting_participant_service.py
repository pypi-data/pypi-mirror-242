from typing import Optional, Union, Dict, Type

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import BaseSerializer

from modules.core.models import User


class VotingParticipantService(object):
    """Сервис работы с участниками голосования"""

    def __init__(self, queryset: QuerySet, serializer_class: Type[BaseSerializer]):
        self.queryset = queryset
        self.serializer_class = serializer_class
        self.model = type(queryset)

    def create_voting_participant_from_user(
        self, user_pk: Union[str, int], comment: Optional[str] = None
    ) -> Dict:
        user = User.objects.filter(pk=user_pk).last()

        if not user:
            raise ValidationError(f"user with pk `{user_pk}` does not exist")
        data = {
            "last_name": user.last_name,
            "first_name": user.first_name,
            "patronymic_name": user.patronymic_name,
            "email": user.email,
            "phone": user.phone,
            "comment": comment,
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
