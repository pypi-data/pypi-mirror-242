from django.contrib import admin

from django.contrib.gis import forms

from modules.plans.models import Location


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

    class Meta:
        model = Location
        fields = [
            "address",
            "gis_point",
            "gis_polygon",
        ]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        "plan",
        "address",
    ]
    form = LocationAdminForm
