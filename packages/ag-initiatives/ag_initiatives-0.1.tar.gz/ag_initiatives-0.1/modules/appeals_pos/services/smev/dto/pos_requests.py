from typing import Optional, Union, List

from lxml import etree
from pydantic import BaseModel

from config.settings import settings
from modules.appeals_pos.services.xml_service import XMLService


class PosStruct(BaseModel):
    def to_dict(self) -> dict:
        return self.dict()

    @classmethod
    def from_dict(cls, data: Union[dict, list, None]):
        return cls.parse_obj(data)

    def to_xml_by_template(self, template_path):
        xml = etree.parse(template_path, etree.XMLParser()).getroot()
        XMLService.insert_dict_in_etree(xml, self.to_dict())
        str_xml: str = etree.tostring(xml, encoding="unicode")
        str_xml = str_xml.replace('env="TEST"', f'env="{settings.POS_ENV}"')
        return str_xml.encode('utf-8')


class OrganizationInfoStruct(PosStruct):
    Ogrn: str = settings.POS_ORGN


class ApplicantDataStruct(PosStruct):
    EpguId: int
    Name: str
    Email: str
    Surname: Optional[str]
    Patronymic: Optional[str]
    Phone: Optional[str]


class AttachmentStruct(PosStruct):
    Name: str
    AttachmentUuid: str


class FileUploadStruct(PosStruct):
    File: AttachmentStruct


class FileUploadRequest(PosStruct):
    File: List[AttachmentStruct]
    ClientId: str = settings.POS_CLIENT_ID


class FileStruct(PosStruct):
    FileId: List[str]


class FileDownloadRequest(PosStruct):
    FileId: List[str]
    ClientId: str = settings.POS_CLIENT_ID


class AppealDataStruct(PosStruct):
    Id: str
    Description: str
    CreatedAt: str
    Applicant: ApplicantDataStruct
    SubjectId: Optional[int]
    SubsubjectId: Optional[int]
    AttachmentIds: Optional[FileStruct]
    Location: Optional[str]
    OrganizationInfo: OrganizationInfoStruct = OrganizationInfoStruct()
    RegionId: int = 24
    ClientId: str = settings.POS_CLIENT_ID


class GetAppealRequest(PosStruct):
    AppealId: str
    ClientId: str = settings.POS_CLIENT_ID
