from dal import autocomplete
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from modules.ecology.models import Event


class EventForm(forms.ModelForm):
    def clean(self) -> None:
        category = self.cleaned_data.get("category")
        organization = self.cleaned_data.get("organization")
        locality = self.cleaned_data.get("locality")
        if not hasattr(organization, "sub_permissions"):
            raise ValidationError({"organization": "Не удалось получить доп права"})
        elif category not in organization.sub_permissions.suggestion_categories.all():
            raise ValidationError({"category": "Выбрана недоступная категория."})
        elif locality not in organization.locality.all():
            raise ValidationError({"locality": "Выбрано недоступное МО."})
        return super().clean()

    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            'category': autocomplete.ModelSelect2(
                url='organization_eventcategory_autocomplete',
                forward=['organization']
            ),
            'locality': autocomplete.ModelSelect2(
                url='organization_locality_autocomplete',
                forward=['organization']
            ),
        }


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    form = EventForm
    list_per_page = 25

    change_list_template = "ecology/admin/model_change_list.html"
    change_form_template = "ecology/admin/map_change_form.html"

    list_display = [
        "id",
        "name",
        "category",
        "locality",
        "start_date",
        "expiry_date",
        "reward",
    ]

    list_filter = ("name", "category", "start_date", "reward", "locality")

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["organization"].label = "Организатор"
        return form
