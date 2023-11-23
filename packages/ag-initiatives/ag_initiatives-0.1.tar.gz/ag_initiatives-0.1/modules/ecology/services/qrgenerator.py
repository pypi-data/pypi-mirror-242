import re
from io import BytesIO, StringIO


import qrcode
import qrcode.image.svg


class QRGenerator:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def get_host(request=None):
        host = "http://24ag.ru/"
        if request:
            host = request.get_host()
            if request.is_secure():
                host = f"https://{host}/"
            else:
                host = f"http://{host}/"
        return host

    @property
    def svg(self):
        factory = qrcode.image.svg.SvgImage
        stream = BytesIO()
        img = qrcode.make(self.data, image_factory=factory)
        img.save(stream)
        qrcode_svg = stream.getvalue().decode()
        return qrcode_svg
