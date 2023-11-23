from adminsortable.admin import SortableStackedInline, NonSortableParentAdmin
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django_summernote.admin import SummernoteModelAdminMixin

from modules.core.models import ActiveCitizenModule
from modules.core.models import ProjectInfo
from modules.core.models.active_citizen_module import ActiveCitizenModuleEnum
from modules.core.models.project_info import BlockFile, BlockLink


class ActiveCitizenModuleForm(forms.ModelForm):
    fields = [
        "name",
    ]

    class Meta:
        model = ActiveCitizenModule
        fields = [
            "name",
            "display_name",
            "is_worked",
        ]


def enable_module(model_admin, request, queryset):
    queryset.update(is_worked=True)


enable_module.short_description = (
    f"Подключить выбранные {ActiveCitizenModule._meta.verbose_name_plural}"
)


def disable_module(model_admin, request, queryset):
    queryset.update(is_worked=False)


disable_module.short_description = (
    f"Отключить выбранные {ActiveCitizenModule._meta.verbose_name_plural}"
)


class ProjectInfoForm(forms.ModelForm):
    class Meta:
        model = ProjectInfo
        fields = '__all__'


@admin.register(BlockFile)
class BlockFileAdmin(admin.ModelAdmin):
    pass


@admin.register(BlockLink)
class BlockLinkAdmin(admin.ModelAdmin):
    pass


class ProjectInfoInline(SummernoteModelAdminMixin, SortableStackedInline):
    model = ProjectInfo
    extra = 0
    verbose_name = 'Блок'
    verbose_name_plural = 'Блоки раздела'
    summernote_fields = ["text"]


@admin.register(ActiveCitizenModule)
class ActiveCitizenModuleAdmin(NonSortableParentAdmin):
    change_form_template = "core/admin/active_citizen_module/change_form.html"
    change_list_template = "core/admin/active_citizen_module/change_list.html"

    inlines = (ProjectInfoInline,)
    form = ActiveCitizenModuleForm
    list_display = ("display_name", 'name', "is_worked")
    list_filter = ("is_worked",)
    actions = [enable_module, disable_module]
    list_editable = ("is_worked",)
    fields = [
        "display_name",
        "name",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.display_name:
            obj.display_name = ActiveCitizenModuleEnum.RESOLVER[obj.name]

        if not obj.id:
            objects = ActiveCitizenModule.objects.filter(Q(name=obj.name), ~Q(name=ActiveCitizenModuleEnum.NEW_MODULE))
        else:
            objects = ActiveCitizenModule.objects.filter(Q(name=obj.name), ~Q(id=obj.id),
                                                         ~Q(name=ActiveCitizenModuleEnum.NEW_MODULE))
        if objects:
            self.message_user(
                request,
                f"Модуль '{ActiveCitizenModuleEnum.RESOLVER[objects.first().name]}' уже существует",
                level=messages.ERROR,
            )
        else:
            obj.save()
            update_data = {
                'is_project_info': False,
            }
            if obj.name == ActiveCitizenModuleEnum.ABOUT_PROJECT:
                update_data['is_project_info'] = True
            obj.blocks.update(**update_data)
