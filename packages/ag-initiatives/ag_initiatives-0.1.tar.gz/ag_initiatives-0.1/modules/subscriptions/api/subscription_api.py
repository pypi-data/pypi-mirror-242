from collections import OrderedDict
from typing import Optional, Union

import django_filters
from django.db.models import QuerySet
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from modules.subscriptions.api.serializers import SubscriptionSerializer
from modules.subscriptions.enums import EventEnum, ActiveCitizenModuleEnum
from modules.subscriptions.models import Subscription, SubscriptionTemplate


class SubscriptionAPI(viewsets.ModelViewSet):
    """Подписки"""

    queryset = Subscription.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = [
        "user",
    ]

    class Meta:
        model = Subscription

    @classmethod
    def _get_module(cls, event: str) -> Optional[str]:
        module = None
        if event in EventEnum.VOTING:
            module = ActiveCitizenModuleEnum.core
        if event in EventEnum.INITIATIVES:
            module = ActiveCitizenModuleEnum.initiatives
        if event in EventEnum.PLANS:
            module = ActiveCitizenModuleEnum.plans
        if event in EventEnum.MAP_WORKS:
            module = ActiveCitizenModuleEnum.ap_works
        if event in EventEnum.NEWS:
            module = ActiveCitizenModuleEnum.core
        return module

    @classmethod
    def _get_template(cls, event: str) -> Union[SubscriptionTemplate, QuerySet]:
        template = SubscriptionTemplate.objects.none()
        if event in EventEnum.START_EVENT:
            template = SubscriptionTemplate.objects.filter(
                event_type="START_EVENT"
            ).first()
        if event in EventEnum.PUBLISH_EVENT:
            template = SubscriptionTemplate.objects.filter(
                event_type="PUBLISH_EVENT"
            ).first()
        if event in EventEnum.END_EVENT:
            template = SubscriptionTemplate.objects.filter(
                event_type="END_EVENT"
            ).first()
        return template

    def create(self, request: Request, *args, **kwargs):
        try:
            user = request.user
            request_data = request.data
            request_data["user"] = user.pk
            event = request_data["event"]
            request_data["module"] = self._get_module(event)
            request_data["template"] = self._get_template(event)
            serializer = self.serializer_class(data=request_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            response_status = status.HTTP_201_CREATED
        except Exception as e:
            data = OrderedDict(
                {
                    "error": f"Subscription Create Exception ({e})",
                    "data": request.data,
                }
            )
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(data, status=response_status)
