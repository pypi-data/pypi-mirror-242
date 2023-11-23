import nested_admin
from django import forms
from django.contrib import admin
from django.forms import TextInput
from django.http import HttpResponse
from django.utils import timezone

from modules.ecology.models import SurveyQuestionAnswer, SurveyQuestion, Survey


class SurveyQuestionAnswerAdminForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestionAnswer
        fields = "__all__"
        widgets = {
            "text": TextInput(attrs={"size": 70}),
            "group": TextInput(attrs={"size": 70}),
        }


class SurveyQuestionAdminForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestion
        fields = "__all__"
        widgets = {
            "text": TextInput(attrs={"size": 70}),
        }


class SurveyAdminForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = "__all__"
        widgets = {"name": TextInput(attrs={"size": 70})}


class SurveyQuestionAnswerAdmin(nested_admin.NestedStackedInline):
    form = SurveyQuestionAnswerAdminForm
    model = SurveyQuestionAnswer
    extra = 0


class SurveyQuestionAdmin(nested_admin.NestedStackedInline):
    form = SurveyQuestionAdminForm
    model = SurveyQuestion
    extra = 0
    inlines = [SurveyQuestionAnswerAdmin]


@admin.register(Survey)
class SurveyAdmin(nested_admin.NestedModelAdmin):
    list_display = [
        "name",
    ]

    form = SurveyAdminForm
    inlines = [SurveyQuestionAdmin]
