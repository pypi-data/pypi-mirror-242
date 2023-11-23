from django.contrib import admin
from django import forms

from modules.feedback.models import Problematic


class ProblematicForm(forms.ModelForm):
    class Meta:
        model = Problematic
        fields = "__all__"


@admin.register(Problematic)
class ProblematicAdmin(admin.ModelAdmin):
    form = ProblematicForm
    list_display = ("id", "name")
    search_fields = (
        "id",
        "name",
    )
    list_filter = (
        # 'is_actual',
        # 'assignment_date',
    )
