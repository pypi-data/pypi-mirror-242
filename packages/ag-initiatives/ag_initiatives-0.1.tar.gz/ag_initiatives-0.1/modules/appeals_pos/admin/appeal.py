import mimetypes
from urllib.parse import quote

import nested_admin
from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse, re_path
from django.utils import html

from config.settings import MEDIA_URL, BASE_DIR
from modules.appeals_pos.admin.actions.reports import appeals_report_with_files, appeals_report
from modules.appeals_pos.models.appeal import SmevState, AppealState
from modules.appeals_pos.models.file import File
from modules.appeals_pos.models import Appeal, AppealStateChange, AppealAnswer, AppealAttachment
from modules.appeals_pos.models.subcategory import Subcategory


def appeal_resend(modeladmin, request, queryset):
    for appeal in queryset:
        appeal.files.update(
            send_to_pos=False,
            smev_adapter_id=None,
            pos_id=None,
        )
        appeal.smev_status = SmevState.PREPARING
        appeal.status = AppealState.MODERATION
        appeal.pos_id = None
        appeal.save()
    modeladmin.message_user(request, f"Объект(ы) успешно обновлен(ы).")


class SubcategoryCategoryNameFilter(admin.SimpleListFilter):
    title = "Категория"
    parameter_name = 'subcategory__category__name'

    def lookups(self, request, model_admin):
        categories = Subcategory.objects.all().order_by(
            'category__name'
        ).values_list('category__name', flat=True).distinct()
        return [(category, category) for category in categories]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(subcategory__category__name=value)


class SubcategoryNameFilter(admin.SimpleListFilter):
    title = "Подкатегория"
    parameter_name = 'subcategory__name'

    def lookups(self, request, model_admin):
        categories = Subcategory.objects.all().order_by('name').values_list('name', flat=True).distinct()
        return [(category, category) for category in categories]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(subcategory__name=value)


class AppealAttachmentInline(nested_admin.NestedStackedInline):
    model = AppealAttachment
    fields = ["file"]
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class AppealAnswerInline(nested_admin.NestedStackedInline):
    model = AppealAnswer
    extra = 0
    inlines = [AppealAttachmentInline]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class AppealStateChangeInline(nested_admin.NestedStackedInline):
    model = AppealStateChange
    extra = 0
    inlines = [AppealAnswerInline]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Appeal)
class AppealAdmin(nested_admin.NestedModelAdmin):
    inlines = [AppealStateChangeInline]
    list_filter = (
        "creation_date_time",
        "status",
        SubcategoryCategoryNameFilter,
        SubcategoryNameFilter,
    )
    list_display = (
        "pos_id",
        "creation_date_time",
        "user_fio",
        "user_email",
        "category",
        "subcategory",
        "status",
    )
    search_fields = (
        "pos_id",
        "user__first_name",
        "user__last_name",
        "user__patronymic_name",
        "user__email",
        "user__phone",
        "address",
    )
    fieldsets = (
        [None, {
            "fields": [
                "pos_id",
                "creation_date_time",
                "user_last_name",
                "user_first_name",
                "user_patronymic_name",
                "user_phone",
                "user_email",
                "category",
                "subcategory",
                "text",
                "files_field",
                "address",
                "to_publish",
                "smev_status",
                "status",
                "answer"
            ]
        }],
    )

    readonly_fields = (
        "id",
        "pos_id",
        "user_last_name",
        "user_first_name",
        "user_patronymic_name",
        "user_phone",
        "user_email",
        "category",
        "creation_date_time",
        "category",
        "subcategory",
        "text",
        "files_field",
        "address",
        "answer",
        "to_publish",
        "smev_status",
    )

    actions = [appeals_report_with_files, appeals_report, appeal_resend]
    appeals_report_with_files.short_description = "Отчет по обращениям c файлами"
    appeals_report.short_description = "Отчет по обращениям"

    def get_queryset(self, request):
        return (
            super()
                .get_queryset(request)
                .select_related("user", "subcategory", "subcategory__category", )
                .prefetch_related("history__answer")
        )

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            re_path(r'^download-file/(?P<pk>\d+)$', self.download_file,
                    name='applabel_modelname_download-file'),
        ]
        return urls

    def answer(self, obj: Appeal):
        if hasattr(obj, 'history'):
            history = obj.history.order_by('-created_at').first()
            if hasattr(history, 'answer'):
                answer = history.answer
                answer_type_name = answer.answer_type_name if answer.answer_type_name else ''
                answer_reject_reason = answer.reject_reason if answer.reject_reason else ''
                answer_id = answer.id
                if not answer_type_name and not answer_reject_reason:
                    answer_display = answer_id
                else:
                    answer_display = f"{answer_type_name} {answer_reject_reason}"
                answer_url = html.format_html(
                    f'<a href="/admin/appeals_pos/appealanswer/{answer.id}">{answer_display}</a>'
                )
                return answer_url
        return 'Отсутствует'

    @staticmethod
    def download_file(request, pk):
        file = File.objects.get(pk=pk)
        path_to_file = f"{BASE_DIR}{MEDIA_URL}{file.file}"
        content_type, _ = mimetypes.guess_type(path_to_file)
        response = HttpResponse(file.file.read(), content_type=f"{content_type}/force-download")
        response['Content-Disposition'] = f'attachment; filename="{quote(file.name)}"'
        return response

    @staticmethod
    def files_field(obj: Appeal):
        string = '\n'.join(
            f'<a href="{reverse("admin:applabel_modelname_download-file", args=[file.pk])}">{quote(file.name)}</a>'
            for file
            in obj.files.all()
        )
        return html.format_html(string)

    def user_email(self, obj: Appeal):
        return obj.user.email

    def user_first_name(self, obj: Appeal):
        return obj.user.first_name

    def user_last_name(self, obj: Appeal):
        return obj.user.last_name

    def user_patronymic_name(self, obj: Appeal):
        return obj.user.patronymic_name

    def user_fio(self, obj: Appeal):
        user = obj.user
        last_name = f"{user.last_name}" if user.last_name else ""
        first_name = f" {user.first_name}" if user.first_name else ""
        patronymic_name = f" {user.patronymic_name}" if user.patronymic_name else ""
        return last_name + first_name + patronymic_name

    def user_phone(self, obj: Appeal):
        return obj.user.phone

    def category(self, obj: Appeal):
        if obj.subcategory:
            return obj.subcategory.category
        return None

    user_email.short_description = "Email пользователя"
    user_first_name.short_description = "Имя пользователя"
    user_last_name.short_description = "Фамилия пользователя"
    user_patronymic_name.short_description = "Отчество пользователя"
    user_fio.short_description = "ФИО пользователя"
    user_phone.short_description = "Телефон пользователя"
    category.short_description = "Категория"
    answer.short_description = "Ответ на обращение"
    appeal_resend.short_description = "Повторная отправка обращений"

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True
