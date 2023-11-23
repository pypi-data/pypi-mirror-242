import nested_admin
from django.contrib import admin
from django import forms
from django.forms import TextInput

from modules.core.mixins import TrackUserMixin
from modules.voting.mixins.vote_admin_mixin import VoteAdminMixin
from modules.voting.models import VoteLocalQuestion, VoteLocalAnswer, VoteLocal



class VoteLocalAdminForm(forms.ModelForm):
    class Meta:
        model = VoteLocal
        fields = "__all__"
        widgets = {
            "topic": TextInput(attrs={"size": 70}),
            "name": TextInput(attrs={"size": 70}),
        }


class VoteLocalAnswerAdminForm(forms.ModelForm):
    class Meta:
        model = VoteLocalAnswer
        fields = "__all__"
        widgets = {"brief": TextInput(attrs={"size": 70})}


class VoteLocalQuestionAdminForm(forms.ModelForm):
    class Meta:
        model = VoteLocalQuestion
        fields = "__all__"
        widgets = {
            "brief": TextInput(attrs={"size": 70}),
            "name": TextInput(attrs={"size": 70}),
        }


class VoteLocalAnswerAdmin(nested_admin.NestedStackedInline):
    form = VoteLocalAnswerAdminForm
    model = VoteLocalAnswer
    extra = 0


class VoteLocalQuestionAdmin(nested_admin.NestedStackedInline):
    form = VoteLocalQuestionAdminForm
    model = VoteLocalQuestion
    extra = 0
    inlines = (VoteLocalAnswerAdmin,)


@admin.register(VoteLocal)
class VoteLocalAdmin(TrackUserMixin, VoteAdminMixin, nested_admin.NestedModelAdmin):
    form = VoteLocalAdminForm
    list_display = [
        "name",
        "department",
        "category",
        "is_opened",
        "is_published",
        "start_date",
        "end_date",
        "voted_users_count",
        "state",
    ]
    inlines = (VoteLocalQuestionAdmin,)
    # actions = [vote_report, vote_report2]

    def voted_users_count(self, instance):
        return (
            instance.usermunicipalvote_set.filter(locality__in=instance.locality.all())
            .distinct("user")
            .count()
        )
