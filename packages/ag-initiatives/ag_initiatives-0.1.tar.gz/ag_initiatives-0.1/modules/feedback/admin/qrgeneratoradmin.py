import zipfile
from io import BytesIO
import requests as simple_request

from django import forms
from django.db.models import Q
from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from modules.feedback.models import QRGenerator

from dal import autocomplete


class CustomInputField(forms.TextInput):
    def search_full_address(self, keyword):

        url = (
            "https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressHint?"
            "search_string={}"
            "&address_type=2"
        )
        response = simple_request.get(url.format(keyword),
                                          headers={'master-token': "4ad2e4be-7e84-4892-b173-16dce7d0dbe7"})

        addresses = response.json()
        return [item["full_name"] for item in addresses['hints']]

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs)
        js_html = str(html)
        index = js_html.find("text") + len("text") + 1
        action_js_html = (
            f"{js_html[:index]} onchange='checkAddress();'{js_html[index:]}\n"
        )

        addresses = self.search_full_address
        # "<script type=\"text/javascript\">\nvar ar = [{0}];".format(', '.join(['1', '2', '3']))
        java_begin = mark_safe(
            '<script type="text/javascript">'
            "function checkAddress() {\
                  textInput = document.getElementById('id_find_address').value"
        )
        java_second = mark_safe("var ar = [{0}];".format(", ".join(["1", "2", "3"])))
        java_end = mark_safe(
            """
    
                  var s = document.getElementById('id_alt_address');
                  s.innerHTML='';
                  s.hidden = false;
                  for(var i=0; i<ar.length; i++) {
                    var option = document.createElement('option');
                    option.text = ar[i];
                    option.value = ar[i];
                    s.options[s.options.length] = option;
                  }
                };
                function insert_value() {
                  textInput = document.getElementById('id_find_address');
                  var s = document.getElementById('id_alt_address');
                  // var ar = ["apple", "banana", "potatos"];
                  option = s.options.selectedIndex;
                  textInput.value = ar[option];
                };
            </script>
            """
        )

        html = mark_safe(action_js_html)
        return java_begin + java_end + html


class QRGeneratorForm(forms.ModelForm):
    # find_address = forms.CharField(widget=CustomInputField)
    # alt_address = forms.ChoiceField()

    class Meta:
        model = QRGenerator
        fields = "__all__"
        widgets = {
            'problematic': autocomplete.ModelSelect2(url='organization_problematic_autocomplete',
                                                     forward=['organization']),
            'locality': autocomplete.ModelSelect2Multiple(url='organization_locality_autocomplete',
                                                          forward=['organization'])
        }

@admin.register(QRGenerator)
class QRGeneratorAdmin(admin.ModelAdmin):
    change_list_template = "feedback/admin/model_change_list.html"
    change_form_template = "feedback/admin/change_form.html"
    queryset = QRGenerator.objects.all()

    def get_urls(self):
        urls = super(QRGeneratorAdmin, self).get_urls()
        custom_urls = [
            url("export/$", self.qr_export, name="qr_export"),
        ]
        return custom_urls + urls

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def get_qr(self, request=None, queryset=None):
        qr_in_memory_zip = BytesIO()
        zip_file = zipfile.ZipFile(qr_in_memory_zip, "a")
        try:
            for qr_item in queryset:
                bytes_qr = qr_item.get_bytes_qr(request)
                zip_file.writestr(
                    f"QR_for_{qr_item.id} ({qr_item.object_name}).png",
                    bytes_qr.getvalue(),
                )
            zip_file.close()
        except Exception as e:
            print(e)
        response = HttpResponse(qr_in_memory_zip.getvalue())
        response["Content-Disposition"] = "attachment; filename=qr_codes.zip"
        response["Content-Type"] = "application/zip"
        return response

    def qr_export(self, request):
        query = Q()
        path = request.path
        path_split = path.split("/")
        qr_id = [int(item) for item in path_split if item.isdigit()]
        selected_action = dict(request.POST).get("_selected_action", None)
        if len(qr_id) > 0:
            query &= Q(pk__in=qr_id)
        elif selected_action and len(selected_action) > 0:
            query &= Q(pk__in=selected_action)
        queryset = self.queryset.filter(query)
        response = self.get_qr(request, queryset)
        return response

    list_display = (
        "id",
        "object_name",
        "email_of_responsible_person",
        "object_address",
    )
    search_fields = (
        "id",
        "object_name",
        "email_of_responsible_person",
        "object_address",
    )
    list_filter = (
        "object_type",
        "creation_date",
        "last_modified_date",
    )

    form = QRGeneratorForm
    actions = ["get_qr"]

    get_qr.short_description = "Скачать выбранные QR-коды"

    class Meta:
        model = QRGenerator
