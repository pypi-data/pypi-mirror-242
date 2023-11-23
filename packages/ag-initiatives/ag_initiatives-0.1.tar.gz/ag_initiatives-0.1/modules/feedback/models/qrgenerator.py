import qrcode
import urllib.parse
from io import BytesIO

from django.db import models
from django.utils import timezone

from .problematic import Problematic
from .objecttype import ObjectType
from .shortlink import ShortLink
from ...core.models import Organization, Department


class QRGenerator(models.Model):
    object_type = models.ForeignKey(
        ObjectType,
        verbose_name="Тип объекта",
        related_name="qrgenerators",
        on_delete=models.CASCADE,
    )

    object_name = models.CharField(
        verbose_name="Название объекта", null=False, max_length=300
    )
    object_address = models.CharField(
        verbose_name="Адрес объекта", null=False, max_length=600
    )

    email_of_responsible_person = models.EmailField(
        verbose_name="Электронный адрес ответственного лица", null=False, max_length=100
    )

    organization = models.ForeignKey(
        Department,
        verbose_name="Организация",
        related_name="qrgenerators",
        on_delete=models.SET_NULL,
        null=True,
        blank=True

    )

    problematic = models.ForeignKey(
        Problematic,
        verbose_name="Проблематика",
        related_name="qrgenerators",
        on_delete=models.CASCADE,
    )

    creation_date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    last_modified_date = models.DateTimeField(
        verbose_name="Дата последнего изменения", auto_now=True
    )
    locality = models.ManyToManyField(
        to="core.Locality",
        blank=True,
        verbose_name="Муниципальные образования",
        related_name='qrgenerators',
    )

    def __str__(self):
        return f"{self.object_name} - {self.email_of_responsible_person}"

    # @property
    def get_bytes_qr(self, request=None):
        url = "http://24ag.ru/"
        if request:
            url = request.get_host()
            if request.is_secure():
                url = f"https://{url}/"
            else:
                url = f"http://{url}/"
        bytes_qr = BytesIO()
        urlencoded_object_address = urllib.parse.quote_plus(
            self.object_address
        ).replace("+", "%20")
        urlencoded_object_name = urllib.parse.quote_plus(self.object_name).replace(
            "+", "%20"
        )
        url_string = f"your-opinion-creation?"
        # url_string = f'{url}your-opinion-creation?'
        # url_string += f"qr={self.id}"
        url_string += f"object_type={self.object_type.id}"
        url_string += f"&object_name={urlencoded_object_name}"
        url_string += f"&locality={','.join(map(str, self.locality.values_list('id', flat=True)))}"
        url_string += f"&object_address={urlencoded_object_address}"
        url_string += f"&email_of_responsible_person={self.email_of_responsible_person}"
        url_string += f"&problematic={self.problematic.id}"
        # print(url_string)
        new_short = ShortLink()
        new_short.set_short_key(url_string)
        new_short.save()
        short_link = f"{url}api/opinion/url/?short={new_short.short_key}"
        # print(short_link)
        default_qr = qrcode.make(short_link)
        resized_qr = default_qr.resize(size=(210, 210))
        resized_qr.save(bytes_qr, format="png")
        return bytes_qr

    class Meta:
        verbose_name = "Данные QR-кода"
        verbose_name_plural = "Данные QR-кодов"

        indexes = [
            models.Index(
                fields=[
                    "id",
                ]
            ),
        ]
