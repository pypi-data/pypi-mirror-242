import nested_admin
from django.contrib import admin
from django import forms
from django.forms import TextInput

from modules.core.mixins import TrackUserMixin
from modules.voting.mixins.vote_admin_mixin import VoteAdminMixin
from modules.voting.models import VoteRegionalQuestion, VoteRegionalAnswer, VoteRegional


class VoteRegionalAdminForm(forms.ModelForm):
    class Meta:
        model = VoteRegional
        fields = "__all__"
        widgets = {
            "topic": TextInput(attrs={"size": 70}),
            "name": TextInput(attrs={"size": 70}),
        }


class VoteRegionalAnswerAdminForm(forms.ModelForm):
    class Meta:
        model = VoteRegionalAnswer
        fields = "__all__"
        widgets = {"brief": TextInput(attrs={"size": 70})}


class VoteRegionalQuestionAdminForm(forms.ModelForm):
    class Meta:
        model = VoteRegionalQuestion
        fields = "__all__"
        widgets = {
            "brief": TextInput(attrs={"size": 70}),
            "name": TextInput(attrs={"size": 70}),
        }


class VoteRegionalAnswerAdmin(nested_admin.NestedStackedInline):
    form = VoteRegionalAnswerAdminForm
    model = VoteRegionalAnswer
    extra = 0


class VoteRegionalQuestionAdmin(nested_admin.NestedStackedInline):
    form = VoteRegionalQuestionAdminForm
    model = VoteRegionalQuestion
    extra = 0
    inlines = (VoteRegionalAnswerAdmin,)


@admin.register(VoteRegional)
class VoteRegionalAdmin(TrackUserMixin, VoteAdminMixin, nested_admin.NestedModelAdmin):
    form = VoteRegionalAdminForm
    list_display = [
        "name",
        "department",
        "category",
        "is_opened",
        "is_published",
        "start_date",
        "end_date",
        "voted_users_count",
    ]
    inlines = (VoteRegionalQuestionAdmin,)

    def voted_users_count(self, instance):
        return (
            instance.usermunicipalvote_set.filter(municipality__in=instance.municipal_formation.all())
            .distinct("user")
            .count()
        )
