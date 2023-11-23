from django.utils import timezone
import io
from django.http import HttpResponse
import pandas
from pandas import DataFrame
from rest_framework import serializers
from xlsxwriter.worksheet import Worksheet


def json_to_bytes_excel(
    json_data: list, sheet_name: str, header_mapping: dict = None, column_mapping=None
) -> io.BytesIO:
    output = io.BytesIO()

    writer = pandas.ExcelWriter(output, engine="xlsxwriter")

    data_frame: DataFrame = pandas.json_normalize(json_data)
    if header_mapping:
        data_frame.rename(columns=header_mapping, inplace=True)

    data_frame.to_excel(writer, sheet_name=sheet_name, index=False)

    if column_mapping:
        workbook = writer.book
        sheet: Worksheet = writer.sheets[sheet_name]
        alignment_format = workbook.add_format({"valign": "left"})
        if isinstance(column_mapping, list):
            for i in range(len(column_mapping)):
                sheet.set_column(i, i, column_mapping[i])
        elif isinstance(column_mapping, int):
            sheet.set_column(0, 20, column_mapping, alignment_format)

    writer.close()

    return output


def get_excel_response(
    bytes_excel: io.BytesIO, response_status: int, filename: str
) -> HttpResponse:
    today = timezone.now().astimezone().strftime("%d.%m.%Y")
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        status=response_status,
    )
    filename = f"{filename} ({today})"
    response["Content-Disposition"] = 'attachment; filename="{}.xlsx"'.format(filename)
    bytes_excel.seek(0)
    response.write(bytes_excel.read())

    return response


def get_partner_history_excel_response(
    json_data, response_status: int, serializer_class
) -> HttpResponse:
    bytes_excel = json_to_bytes_excel(
        json_data=json_data,
        header_mapping=serializer_class.HEADER_MAPPING,
        sheet_name=serializer_class.SHEET_NAME,
        column_mapping=serializer_class.COLUMN_SIZES,
    )

    return get_excel_response(
        bytes_excel=bytes_excel,
        response_status=response_status,
        filename=serializer_class.FILE_NAME,
    )


class ExcelSerializer(serializers.ModelSerializer):
    """Сериализатор, который переводит данные в excel формат (только на вывод, записать не получится)."""

    HEADER_MAPPING = None
    COLUMN_SIZES = None
    SHEET_NAME = "sheet1"
    FILE_NAME = "Report"

    @classmethod
    def excel_response(cls, json_data, response_status) -> HttpResponse:
        return get_partner_history_excel_response(
            json_data, response_status=200, serializer_class=cls
        )
