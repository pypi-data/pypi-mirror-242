from lxml import etree

from modules.appeals_pos.services.xml_service import XMLService


class BaseResponseStrategy:
    TAG = "Envelope"

    @classmethod
    def get_current_block(cls, xml):
        if block := xml.xpath(f'//*[local-name()="{cls.TAG}"]'):
            return block[0]
        return None

    @classmethod
    def is_current(cls, xml: etree.ElementBase):
        block = cls.get_current_block(xml)
        return block is not None

    @classmethod
    def process_response(cls, xml):
        block = cls.get_current_block(xml)
        return XMLService.xml_to_dict(block)
