import nested_admin
from django.contrib import admin
from django import forms
from django.forms import TextInput

from modules.core.mixins import TrackUserMixin
from modules.voting.mixins.municipal_vote_mixin_admin import MunicipalVoteAdminMixin
from modules.voting.models import VoteMunicipalQuestion, VoteMunicipalAnswer, VoteMunicipal



class VoteMunicipalAdminForm(forms.ModelForm):
    class Meta:
        model = VoteMunicipal
        fields = "__all__"
        widgets = {
            "topic": TextInput(attrs={"size": 70}),
            "name": TextInput(attrs={"size": 70}),
        }


class VoteMunicipalAnswerAdminForm(forms.ModelForm):
    class Meta:
        model = VoteMunicipalAnswer
        fields = "__all__"
        widgets = {"brief": TextInput(attrs={"size": 70})}


class VoteMunicipalQuestionAdminForm(forms.ModelForm):
    class Meta:
        model = VoteMunicipalQuestion
        fields = "__all__"
        widgets = {
            "brief": TextInput(attrs={"size": 70}),
            "name": TextInput(attrs={"size": 70}),
        }


class VoteMunicipalAnswerAdmin(nested_admin.NestedStackedInline):
    form = VoteMunicipalAnswerAdminForm
    model = VoteMunicipalAnswer
    extra = 0


class VoteMunicipalQuestionAdmin(nested_admin.NestedStackedInline):
    form = VoteMunicipalQuestionAdminForm
    model = VoteMunicipalQuestion
    extra = 0
    inlines = (VoteMunicipalAnswerAdmin,)


@admin.register(VoteMunicipal)
class VoteMunicipalAdmin(TrackUserMixin, MunicipalVoteAdminMixin, nested_admin.NestedModelAdmin):
    form = VoteMunicipalAdminForm
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
    inlines = (VoteMunicipalQuestionAdmin,)
    # actions = [vote_report, vote_report2]

    def voted_users_count(self, instance):
        return (
            instance.usermunicipalvote_set.filter(locality__in=instance.locality.all())
            .distinct("user")
            .count()
        )
