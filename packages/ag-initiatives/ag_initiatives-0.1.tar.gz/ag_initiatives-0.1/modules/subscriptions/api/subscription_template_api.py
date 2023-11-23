from typing import List

from django.db.models import QuerySet
from rest_framework import viewsets, permissions

from modules.subscriptions.api.serializers import SubscriptionTemplateSerializer
from modules.subscriptions.models import SubscriptionTemplate


class SubscriptionTemplateAPI(viewsets.ModelViewSet):
    """Шаблон сообщения подписки"""

    queryset: QuerySet = SubscriptionTemplate.objects.all()
    permission_classes: List = [permissions.IsAuthenticated]
    serializer_class: SubscriptionTemplateSerializer = SubscriptionTemplateSerializer
    http_method_names: List[str] = ["get"]
