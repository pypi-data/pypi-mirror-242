from django.template.loader import render_to_string
from weasyprint import HTML


def build_pdf(serialized_data):
    filename = f'Инициатива_{serialized_data["number"]}.pdf'
    output = HTML(
        string=render_to_string("initiative_pdf.html", context=serialized_data)
    ).write_pdf()
    return filename, output
