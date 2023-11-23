from django.contrib import admin
from django import forms

from modules.core.mixins import TrackUserMixin
from modules.core.models import Locality
from ag_initiatives.modules.initiatives.models import InitiativeAcceptingSettings


class InitiativeAcceptingSettingsForm(forms.ModelForm):
    locality = forms.ModelChoiceField(
        queryset=Locality.objects.all(),
        label='Муниципальные образования',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('instance', None):
            locale = kwargs['instance'].locality.all()[0]
            self.initial['locality'] = locale
            self.fields['locality'].initial = locale

    def clean(self):
        self._validate_unique = True
        locality = self.cleaned_data.get('locality', None)
        if locality:
            self.cleaned_data['locality'] = [locality]
        return self.cleaned_data

    class Meta:
        model = InitiativeAcceptingSettings
        fields = (
            'department',
            'locality',
            'category',
            'duration_month',
            'votes_threshold',
            'active',
        )

@admin.register(InitiativeAcceptingSettings)
class InitiativeAcceptingSettingsAdmin(TrackUserMixin, admin.ModelAdmin):
    form = InitiativeAcceptingSettingsForm
    list_display = [
        "active",
        "department",
        "locality_",
        "parent_category",
        "category",
        "duration_month",
        "votes_threshold",
    ]

    def locality_(self, instance: InitiativeAcceptingSettings):
        if instance.locality.exists():
            # return ', '.join(
            #     [locality.name for locality in instance.locality.all()])
            return instance.locality.all()[0].name
    locality_.short_description = "Муниципальные образования"

    def parent_category(self, obj: InitiativeAcceptingSettings):
        return obj.category.parent
