from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.html import XmlLexer
import xml.dom.minidom
from django.utils.safestring import mark_safe
from django.contrib import admin

from modules.appeals_pos.models import SmevLog


@admin.register(SmevLog)
class SmevLogAdmin(admin.ModelAdmin):

    def _data(self, instance):
        try:
            if not instance.xml_data:
                return ""
            dom = xml.dom.minidom.parseString(instance.xml_data)
            pretty_xml = dom.toprettyxml()
            formatter = HtmlFormatter(style='colorful')
            output = highlight(pretty_xml, XmlLexer(), formatter)
            style = "<style>" + formatter.get_style_defs() + "</style><br>"
            return mark_safe(style + output)
        except Exception as err:
            from sentry_sdk import capture_exception
            capture_exception(err)
            return ""

    _data.short_description = "Переданные данные"

    readonly_fields = (
        '_data',
        'created_at',
        'updated_at',
        'description',
    )
    list_display = (
        "updated_at",
        "created_at",
        "description",
    )
    search_fields = (
        "xml_data",
        "description",
    )

    fieldsets = (
        ('Дата создания', {"fields": ("created_at", "updated_at")}),
        ('Данные', {"fields": ("description", "_data")}),
    )

    ordering = ("-updated_at",)

    def has_add_permission(self, request):
        return False
