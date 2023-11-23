import io
import os
import zipfile
from urllib.parse import quote

from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils import timezone
from requests import Request

from modules.appeals_pos.models import AppealAttachment
from modules.appeals_pos.serializers import AppealExcelSerializer
from modules.ecology.api.serializers.excel import json_to_bytes_excel


def appeals_report_with_files(modeladmin, request, queryset):
    """Формирование отчета и вложенных файлов для скачивания"""
    xlsx_io = make_xlsx_report(queryset, request)
    zip_buffer = io.BytesIO()
    zip_archive = zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED)
    attachments = []
    for appeal in queryset.filter(files__isnull=False).prefetch_related("files"):
        appeal_attachments = AppealAttachment.objects.filter(appeal_answer__appeal_state_change__appeal=appeal).distinct()
        for attachment in appeal_attachments:
            try:

                filename = (
                    f"Файлы_ответов/{appeal.pos_id}/{os.path.basename(attachment.file_name)}"
                )

                if filename in list(
                        map(lambda _attachment: _attachment[0], attachments)
                ):
                    continue

                attachment_buffer = io.BytesIO()
                file = attachment.file.file.read()
                attachment_buffer.write(file)
                attachments.append((filename, attachment_buffer.getvalue()))
            except FileNotFoundError as e:
                print(str(e))
        for attachment in appeal.files.all():
            try:

                filename = (
                    f"Вложения/{appeal.pos_id}/{os.path.basename(attachment.file.name)}"
                )

                if filename in list(
                        map(lambda _attachment: _attachment[0], attachments)
                ):
                    continue

                attachment_buffer = io.BytesIO()
                file = attachment.file.file.read()
                attachment_buffer.write(file)
                attachments.append((filename, attachment_buffer.getvalue()))
            except FileNotFoundError as e:
                print(str(e))

    for attachment in set(attachments):
        zip_archive.writestr(attachment[0], attachment[1])
    today = timezone.now().astimezone().strftime("%d.%m.%Y")

    zip_archive.writestr(
        f"Отчет по обращениям {today}.xlsx", xlsx_io.getvalue()
    )
    zip_archive.close()

    response = HttpResponse(content_type="application/zip", status=200)
    filename = f"Отчет по обращениям с вложением {today}"
    response["Content-Disposition"] = f'attachment; filename="{quote(filename)}.zip"'
    response.write(zip_buffer.getvalue())

    return response


def appeals_report(modeladmin, request, queryset):
    """Формирование отчета для скачивания"""
    xlsx_io = make_xlsx_report(queryset, request)

    today = timezone.now().astimezone().strftime("%d.%m.%Y")
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    filename = f"Отчет по обращениям {today}"
    response["Content-Disposition"] = f'attachment; filename="{quote(filename)}.xlsx"'
    response.write(xlsx_io.getvalue())

    return response


def make_xlsx_report(queryset: QuerySet, request: Request) -> io.BytesIO:
    """Создание xlsx отчета по queryset"""
    json_data = AppealExcelSerializer(
        queryset.select_related(
            "user", "subcategory", "subcategory__category"
        ).prefetch_related("files", "history"),
        many=True,
        context={"request": request},
    ).data
    xlsx_buffer = json_to_bytes_excel(
        json_data,
        AppealExcelSerializer.SHEET_NAME,
        header_mapping=AppealExcelSerializer.HEADER_MAPPING,
        column_mapping=AppealExcelSerializer.COLUMN_SIZES,
    )
    return xlsx_buffer
