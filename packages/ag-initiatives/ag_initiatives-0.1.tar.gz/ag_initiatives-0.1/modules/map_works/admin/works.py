import nested_admin
from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.contrib.gis import forms
from django.db.models import Q
from rangefilter.filters import DateTimeRangeFilter

from modules.core.mixins import TrackUserMixin
from modules.map_works.api.serializers.works import WorksExcelSerializer
from modules.map_works.models import Works, Location


class LocationAdminForm(forms.ModelForm):
    gis_point = forms.PointField(
        required=False,
        widget=forms.OSMWidget(
            attrs={
                "default_lon": 92.86717,
                "default_lat": 56.01839,
                "default_zoom": 12,
                "map_srid": 4326,
            }
        ),
    )
    gis_polygon = forms.PolygonField(
        required=False,
        widget=forms.OSMWidget(
            attrs={
                "default_lon": 92.86717,
                "default_lat": 56.01839,
                "default_zoom": 12,
                "map_srid": 4326,
            }
        ),
    )


class LocationAdmin(nested_admin.NestedStackedInline):
    model = Location
    extra = 0
    # form = LocationAdminForm # todo


def works_report(modeladmin, request, queryset):
    if queryset.count() == 0:
        return

    data = WorksExcelSerializer(queryset, many=True).data
    response = WorksExcelSerializer.excel_response(data, response_status=200)
    return response


works_report.short_description = "Отчет по ремонтным работам"


class WorksDateTimeFilter(DateTimeRangeFilter):
    def __init__(self, *args, **kwargs):
        super(WorksDateTimeFilter, self).__init__(*args, **kwargs)
        self.title = "Дата-время"

    def queryset(self, request, queryset):
        if self.form.is_valid():
            validated_data = dict(self.form.cleaned_data.items())
            if not validated_data:
                return queryset

            begin_date_value = validated_data.get(self.lookup_kwarg_gte, None)
            end_date_value = validated_data.get(self.lookup_kwarg_lte, None)
            predicates = []

            if begin_date_value:
                predicates.append((Q(begin_datetime__gte=begin_date_value) | Q(end_datetime__gte=begin_date_value)))

            if end_date_value:
                predicates.append((Q(begin_datetime__lte=end_date_value) | Q(end_datetime__lte=end_date_value)))

            return queryset.filter(*predicates)

        return queryset


@admin.register(Works)
class WorksAdmin(TrackUserMixin, nested_admin.NestedModelAdmin):
    list_display = [
        "locality",
        "category",
        "reason",
        "begin_datetime",
        "end_datetime",
        "private_territory",
        "institution_type",
        "work_type",
        "contractor",
        "is_published",
    ]

    list_filter = [
        ("begin_datetime", WorksDateTimeFilter),
        "category",
        "reason",
        "work_type",
        "locality"
    ]

    inlines = [LocationAdmin]

    actions = [works_report]
