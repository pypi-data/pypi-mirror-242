from django_filters import rest_framework as filters
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.filters import NewsFilter
from modules.api.pagination import DefaultPagination
from modules.api.serializers import (
    NewsSerializer,
    NewsShortSerializer,
    NewsCreateSerializer,
)
from modules.core.models import News
from modules.core.permissions import IsOperator


class NewsViewSet(mixins.DestroyModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all().order_by("-create_date").filter()
    serializer_class = NewsSerializer
    pagination_class = DefaultPagination
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = NewsFilter

    def get_serializer_class(self):
        return NewsSerializer if self.action == "retrieve" else NewsShortSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsOperator]
        return super().get_permissions()

    def create(self, request: Request):
        serializer = NewsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        # TrackUserApiMixin.create(request, instance, None, False)
        # TODO разобраться почему это не работает
        return Response(self.serializer_class(instance).data)

    def update(self, request: Request, pk: int):
        instance = News.objects.filter(pk=pk).first()
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data._mutable = True

        if data.get('image') is None:
            data['image'] = None
        elif data.get('image') == '':
            data.pop('image')

        if data.get('video_id') == '':
            data['video_id'] = None

        if data.get('audio_id') == '':
            data['audio_id'] = None

        data._mutable = False

        serializer = NewsCreateSerializer(
            data=request.data,
            instance=instance,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        # TrackUserApiMixin.create(request, updated_instance, None, True)
        # TODO разобраться почему это не работает
        return Response(self.serializer_class(updated_instance).data)
