import json

from django.db import transaction
from django.db.models import (
    Func,
    F,
    Value,
    ExpressionWrapper,
    DateTimeField,
    IntegerField,
    DateField,
    DurationField,
)
from django.db.models.expressions import RawSQL
from django.db.models.functions import Cast
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.core.models import User, UserRole
from modules.core.permissions import IsOperator
from modules.map_works.api.filters import WorksFilter
from modules.map_works.api.serializers import (
    WorksDetailsSerializer,
    WorksCreateSerializer,
    LocationMapSerializer,
    WorksList2Serializer,
)
from modules.map_works.models import Works, Location


class WorksAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Works.objects.all()
    serializer_class = WorksList2Serializer
    filterset_class = WorksFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WorksDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def map(self, request):
        works = self.filter_queryset(self.get_queryset())

        locations = Location.objects.filter(
            work__in=works.values_list("id", flat=True), gis_point__isnull=False
        )

        now_time = timezone.now()

        # todo: сделай по нормальному
        if not "completed_date_range_before" in request.query_params:
            locations = locations.annotate(
                edt=Cast("work__end_datetime", DateTimeField()),
                fd=Cast("work__category__display_after_finish_days", IntegerField()),
            ).annotate(
                enddt=ExpressionWrapper(
                    F("edt")
                    + RawSQL(
                        "interval '1 day' * map_works_workcategory.display_after_finish_days",
                        [],
                    ),
                    output_field=DateTimeField(),
                )
            )

            locations = locations.filter(enddt__gte=now_time)

        return Response(LocationMapSerializer(locations, many=True).data)
