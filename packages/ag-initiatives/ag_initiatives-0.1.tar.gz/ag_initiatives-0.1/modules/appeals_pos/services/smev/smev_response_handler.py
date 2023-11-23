from lxml import etree
from requests import Response

from .base_response_strategy import BaseResponseStrategy
from .pos_response_handler import PosResponseStrategy
from .pos_smev_client import PosSmevHttpClient
from ...models import SmevLog


class SmevResponseHandler:
    def __init__(self, response):
        try:
            if isinstance(response, Response):
                self.response_xml = etree.fromstring(response.text.encode('utf-8'))
            elif isinstance(response, str):
                self.response_xml = etree.fromstring(response.encode('utf-8'))
            else:
                self.response_xml = None
        except SyntaxError:
            SmevLog.objects.create(
                description="Неожиданное тело ответа СМЭВ",
                xml_data=response.text
            )
            raise

    def handle_response(self):
        if FaultSmevResponseStrategy.is_current(self.response_xml):
            strategy = FaultSmevResponseStrategy()
        elif SmevFaultSmevResponseStrategy.is_current(self.response_xml):
            strategy = SmevFaultSmevResponseStrategy()
        elif SuccessSmevResponseStrategy.is_current(self.response_xml):
            strategy = SuccessSmevResponseStrategy()
        elif PosResponseStrategy.is_current(self.response_xml):
            strategy = PosResponseStrategy()
        else:
            strategy = BaseResponseStrategy()

        result = strategy.process_response(self.response_xml)
        return result

    def ask_response(self):
        message_metadata = self.response_xml.xpath(f'//*[local-name()="MessageMetadata"]')
        if message_metadata:
            message_id = message_metadata[0].xpath(f'//*[local-name()="MessageId"]')[0].text
            PosSmevHttpClient().ack_request(message_id)


class FaultSmevResponseStrategy(BaseResponseStrategy):
    TAG = "Fault"


class SmevFaultSmevResponseStrategy(BaseResponseStrategy):
    TAG = "SmevFault"


class SuccessSmevResponseStrategy(BaseResponseStrategy):
    TAG = "SendRequestResponse"
