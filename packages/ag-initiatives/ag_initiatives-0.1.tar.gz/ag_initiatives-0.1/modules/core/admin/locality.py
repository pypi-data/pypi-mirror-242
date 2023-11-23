from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.gis import forms
from django.forms import TextInput

from modules.core.mixins import TrackUserMixin
from modules.core.models import Locality, LocalityType, InhabitedLocality
from modules.core.models.locality import LocalityCategory


class MunicipalityAdminForm(forms.ModelForm):
    gis_center = forms.PointField(
        required=False,
        widget=forms.OSMWidget(
            attrs={
                "default_lon": 92.86717,
                "default_lat": 56.01839,
                "default_zoom": 12,
            }
        ),
    )
    gis_border = forms.PolygonField(
        required=False,
        widget=forms.OSMWidget(
            attrs={
                "default_lon": 92.86717,
                "default_lat": 56.01839,
                "default_zoom": 12,
            }
        ),
    )

    class Meta:
        model = Locality
        fields = ["name", "type", "gis_center", "gis_border"]


class LocalityAdminInlineForm(forms.ModelForm):

    class Meta:
        model = Locality
        fields = ["name", "type"]
        widgets = {"name": TextInput(attrs={"size": 70})}


class MunicipalityTypeListFilter(SimpleListFilter):
    title = "Тип"
    parameter_name = "type"

    def lookups(self, request, model_admin):
        types = LocalityType.objects.filter(category=LocalityCategory.MUNICIPALITY).values_list('id', 'name').distinct()
        return types

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(type=self.value())


class LocalityTypeListFilter(SimpleListFilter):
    title = "Тип"
    parameter_name = "type"

    def lookups(self, request, model_admin):
        types = LocalityType.objects.filter(category=LocalityCategory.LOCALITY).values_list('id', 'name').distinct()
        return types

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(type=self.value())


class LocalityInline(admin.TabularInline):
    verbose_name = "Населенный пункт"
    verbose_name_plural = "Населенные пункты"
    model = InhabitedLocality
    fields = ["name", "type"]
    form = LocalityAdminInlineForm
    extra = 0
    show_change_link = True


class LocalityAdminForm(forms.ModelForm):
    class Meta:
        model = Locality
        fields = "__all__"


# @admin.register(Municipality)
# class MunicipalityAdmin(TrackUserMixin, admin.ModelAdmin):
#     search_fields = ["name"]
#     form = MunicipalityAdminForm
#     list_filter = [MunicipalityTypeListFilter]
#     inlines = [LocalityInline]
#     list_display = ["name", "type"]
#     list_per_page = 25


@admin.register(Locality)
class LocalityAdmin(TrackUserMixin, admin.ModelAdmin):
    search_fields = ["name"]
    form = MunicipalityAdminForm
    list_filter = [MunicipalityTypeListFilter]
    list_display = ["name"]
    list_per_page = 25

# @admin.register(InhabitedLocality)
# class LocalityAdmin(TrackUserMixin, admin.ModelAdmin):
#     fields = ["parent", "name", "type", "gis_center", "gis_border"]
#     form = LocalityAdminForm
#     list_display = ["name", "type", "parent"]
#     list_filter = [LocalityTypeListFilter]
#     list_per_page = 25
#     list_select_related = ["parent"]
#     list_editable = ["parent", "type"]
