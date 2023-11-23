from django import forms
from django.contrib import admin
from django.db import models
from django.db.models.query import Q
from django_summernote.admin import SummernoteModelAdmin

from modules.integration.models.external_system import CustomPermission, ExternalSystemToken
from django.contrib.contenttypes.models import ContentType


@admin.register(ExternalSystemToken)
class ExternalSystemAdmin(SummernoteModelAdmin):
    summernote_fields = ["description"]
    formfield_overrides = {
        models.TextField: {"widget": forms.TextInput(attrs={"style": "width: 50em"})},
    }
    filter_horizontal = ("permission",)

    class Meta:
        model = ExternalSystemToken

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        self._change_permission_queryset(form)
        self._change_helped_texts(form)

        return form

    def _change_permission_queryset(self, form):
        content_type = ContentType.objects.get(app_label='integration', model='externalsystemtoken')
        form.base_fields['permission'].queryset = CustomPermission.objects.filter(
            content_type=content_type
        ).filter(~Q(name__istartswith="can"))

    def _change_helped_texts(self, form):
        form.base_fields['key'].help_text = (
            'Ключ - используется для аутентификации в системе. '
            'Максимальная длина 40 символов. '
            'При пустом значении ключ генерируется автоматически при сохранении записи.'
        )
        form.base_fields['url'].help_text = 'Ссылка, которая используется для уведомления об изменениях в Системе.'
