from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.ecology.api.filters import EventFilter
from modules.ecology.api.serializers import EventListSerializer, EventDetailsSerializer
from modules.ecology.models import Event
from django_filters import rest_framework as filters


class EventAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.filter(is_published=True)
    serializer_class = EventListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EventDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})
