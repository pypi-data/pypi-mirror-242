from functools import wraps

from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.templatetags.admin_modify import submit_row
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.db.models import Q, QuerySet
from django.http import QueryDict, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from modules.core.mixins.custom_filter_admin_mixin import CustomListFiltersMixin
from modules.core.mixins.date_list_filter_admin import DateListFilterMixin
from modules.core.models import UserActionTracking
from modules.core.models.user_action_tracking import ActionTypeEnum
from modules.core.services.excelhandler import Excel


@admin.register(UserActionTracking)
class UserActionTrackingAdmin(
    DateListFilterMixin, CustomListFiltersMixin, admin.ModelAdmin
):
    change_list_template = "core/admin/user_action_tracking/model_change_list.html"
    # change_form_template = "core/admin/user_action_tracking/change_form.html"
    list_display = [field.name for field in UserActionTracking._meta.fields]
    list_filter = [
        "timestamp",
    ]
    search_fields = (
        "subject",
        "module",
        "object_name",
        "locality",
        "value_before",
        "value_after",
    )
    readonly_fields = [field.name for field in UserActionTracking._meta.fields]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url("get_excel_report/$", self.get_excel_report, name="get_excel_report"),
        ]
        return custom_urls + urls

    def get_filtered_queryset(self, request, queryset):
        parameter_name = {"parameter_name": key for key in request.GET}.get(
            "parameter_name"
        )
        for item in self.list_filter:
            if item.parameter_name == parameter_name:
                filter_obj = item(
                    request=request, params={}, model=self.model, model_admin=self
                )
                queryset = filter_obj.queryset(request=request, queryset=queryset)
        return queryset

    def fill_excel(self, queryset: QuerySet):
        excel = Excel()
        excel.create()
        row = 0
        excel.add_style(
            name="SimpleHeader",
            font_style="Bold",
            border_style="thin",
            border_color="000000",
            horizontal="center",
            wrap_text=True,
        )
        excel.add_style(
            name="CustomNormal",
            border_style="thin",
            border_color="000000",
            wrap_text=True,
        )
        for column, field in enumerate(self.model._meta.fields):
            excel.edit(row, column, field.verbose_name)
            excel.set_style(row, column, style="SimpleHeader")
            excel.set_height(row, column)
        row += 1
        for item in queryset.order_by("timestamp"):
            for column, field in enumerate(item.__class__._meta.fields):
                string = f"item.{field.name}"
                value = eval(string)
                if value is None:
                    value = ""
                if isinstance(value, timezone.datetime):
                    value = value.astimezone().strftime("%d.%m.%Y %H:%M:%S")
                if field.name == "operation_type":
                    value = ActionTypeEnum.RESOLVER.get(value)

                excel.edit(row, column, str(value))
                excel.set_style(row, column, style="CustomNormal")
                excel.set_width(row, column)
                excel.set_height(row, column)
            row += 1
        excel.save(in_memory=True)
        return excel

    def get_excel_report(self, request):
        query_string = request.GET.get("previous_query_string")
        items_id = [
            int(item) for item in dict(request.GET.copy()).get("_selected_action", [])
        ]
        query = Q()
        if items_id:
            query = Q(pk__in=items_id)
        queryset = self.get_queryset(request).filter(query).distinct()
        if query_string != "":
            query_dict = QueryDict(query_string=query_string)
            request.GET = query_dict
            queryset = self.get_filtered_queryset(request, queryset)
        excel = self.fill_excel(queryset)
        filename = f"User Action Report_{excel.today.isoformat()}.xlsx"
        response = HttpResponse(content_type="application/excel")
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
        response.write(excel.read_data_from_memory())
        return response
