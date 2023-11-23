from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from modules.core.mixins import TrackUserMixin
from modules.core.models import Department, DepartmentSubInfo, LkoLevel, LkoType, DepartmentSubPermissions


class DepartmentAdminInlineForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "status"]
        widgets = {"name": forms.TextInput(attrs={"size": 70})}


class DepartmentAdminInline(admin.TabularInline):
    verbose_name = "Подведомственная организация"
    verbose_name_plural = "Подведомственные организации"
    model = Department
    fields = ["name", "status"]
    form = DepartmentAdminInlineForm
    extra = 1
    show_change_link = True


class DepartmentMainListFilter(SimpleListFilter):
    title = "Основной"
    parameter_name = "main"

    def lookups(self, request, model_admin):
        return (("main", "Основные"),)

    def queryset(self, request, queryset):
        if self.value() == "main":
            return queryset.filter(parent__isnull=True)
        return queryset


class DepartmentSubInfoInline(admin.StackedInline):
    model = DepartmentSubInfo


@admin.register(DepartmentSubInfo)
class DepartmentSubInfoAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


class DepartmentSubPermissionsForm(forms.ModelForm):
    class Meta:
        model = DepartmentSubPermissions
        fields = '__all__'
        widgets = {
            'appeals_categories': forms.SelectMultiple(attrs={'style': 'width: 50vw'})
        }

class DepartmentSubPermissionsInline(admin.StackedInline):
    model = DepartmentSubPermissions
    form = DepartmentSubPermissionsForm

@admin.register(Department)
class DepartmentAdmin(TrackUserMixin, admin.ModelAdmin):
    filter_horizontal = ("locality",)
    list_filter = [DepartmentMainListFilter]
    fieldsets = (
        [
            "Общее",
            {
                "fields": (
                    "parent",
                    "name",
                    "email",
                    "locality",
                    "image",
                    "email_initiative_notification",
                    "status",
                )
            },
        ],
        # [_("Настройки фильтрации"), {"fields": ("categories", "additional_filtering")}],
    )
    inlines = [DepartmentSubInfoInline, DepartmentSubPermissionsInline]

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(DepartmentAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields["categories"].queryset = InitiativeCategory.objects.filter(
    #         ~Q(parent=None)
    #     )
    #     return form


@admin.register(LkoLevel)
class LkoLevelAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = ('name',)


@admin.register(LkoType)
class LkoTypeAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = ('name',)
