from django.contrib import admin
from django import forms

from modules.feedback.models import ShortLink


class ShortLinkForm(forms.ModelForm):
    class Meta:
        model = ShortLink
        fields = "__all__"


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    form = ShortLinkForm
    list_display = (
        "id",
        "short_key",
        "active",
        "validity_period",
        "counter",
    )
    search_fields = (
        "id",
        "short_key",
    )
    list_filter = (
        "active",
        # 'assignment_date',
    )

    def get_actions(self, request):
        actions = super(ShortLinkAdmin, self).get_actions(request)
        del actions["delete_selected"]
        return actions


def has_delete_permission(request, obj=None):
    return False
