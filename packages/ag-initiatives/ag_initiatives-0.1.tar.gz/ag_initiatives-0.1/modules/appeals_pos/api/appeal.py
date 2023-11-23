from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from modules.appeals_pos.filters import AppealFilter
from modules.appeals_pos.models import AppealStateChange, Appeal
from modules.appeals_pos.pagination import DefaultPagination
from modules.appeals_pos.serializers import (
    AppealFullSerializer,
    AppealWriteSerializer,
)
from modules.appeals_pos.serializers.appeal_notification import (
    AppealNotificationSerializer,
)
from modules.appeals_pos.services.appeal_service import AppealService


class AppealApi(viewsets.ModelViewSet):
    paginator = DefaultPagination()
    queryset = Appeal.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AppealFilter
    service = AppealService()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["my_appeals", "retrieve"]:
            return AppealFullSerializer
        if self.action == "create":
            return AppealWriteSerializer
        return AppealFullSerializer

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.service.get_published_appeals())
        page = self.paginator.paginate_queryset(queryset, request=request)
        serializer = self.get_serializer_class()(page, many=True)
        response = self.paginator.get_paginated_response(serializer.data)
        return response

    def retrieve(self, request: Request, *args, **kwargs):
        appeal = self.get_object()
        serializer = self.get_serializer_class()(appeal)
        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=["get"], detail=False, url_path="my")
    def my_appeals(self, request: Request):
        queryset = self.filter_queryset(self.service.get_user_appeals(request.user))
        page = self.paginator.paginate_queryset(queryset, request=request)
        serializer = self.get_serializer_class()(page, many=True)
        response = self.paginator.get_paginated_response(serializer.data)
        return response

    @action(methods=["get"], detail=False)
    def my_pos_notifications(self, request):
        user_appeals = self.service.get_user_appeals(request.user)
        queryset = AppealStateChange.objects.filter(appeal__in=user_appeals).order_by(
            "-created_at"
        )
        return Response(AppealNotificationSerializer(queryset, many=True).data)

    @action(methods=["get"], detail=False)
    def count(self, request: Request):
        queryset = self.service.get_user_appeals(request.user)
        return Response({"count": queryset.count()})
