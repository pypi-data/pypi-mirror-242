from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.pagination import DefaultPagination
from modules.core.models import User, Locality
from modules.core.permissions import IsOperator
from modules.feedback.api.v1.filters import OpinionFilters
from modules.feedback.api.v1.serializers import OpinionSerializer
from modules.feedback.models import Opinion
from modules.voting.api.serializers import (
    LocalityDetailsSerializer
)


class OpinionModeratorAPI(viewsets.ReadOnlyModelViewSet):
    """API для мнений Модератора"""
    queryset = Opinion.objects.none()
    permission_classes = [IsOperator]
    filterset_class = OpinionFilters
    serializer_class = OpinionSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        return Opinion.objects.all().distinct().order_by("-placement_date").prefetch_related("locality")

    def list(self, request: Request, *args, **kwargs):
        paginator = self.pagination_class()

        queryset = self.get_queryset()

        opinions = self.filterset_class(
            data=request.query_params,
            queryset=queryset,
        ).qs

        page = paginator.paginate_queryset(queryset=opinions, request=request)
        serializer = self.serializer_class(page, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return response

    @action(methods=["get"], detail=False, url_path="info")
    def info(self, request: Request, *args, **kwargs):
        user: User = request.user

        data = {
            "localities": LocalityDetailsSerializer(Locality.objects.all(), many=True).data,
        }
        return Response(data)
