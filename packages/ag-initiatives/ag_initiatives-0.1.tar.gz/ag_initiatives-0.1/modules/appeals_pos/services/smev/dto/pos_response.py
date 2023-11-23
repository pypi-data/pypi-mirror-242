from typing import Union, List

from pydantic import BaseModel, validator
from pydantic.fields import SHAPE_LIST


class PosStruct(BaseModel):
    def to_dict(self) -> dict:
        return self.dict()

    @classmethod
    def from_dict(cls, data: Union[dict, list, None]):
        return cls.parse_obj(data)

    @validator("*", pre=True, always=True, allow_reuse=True)
    def wrap_list(cls, value, field):
        if field.shape == SHAPE_LIST and not isinstance(value, list):
            return [value]
        return value


class FileDTO(BaseModel):
    Id: str = None
    Name: str = None
    Size: str = None
    MimeType: str = None
    AttachmentUuid: str = None


class FileUploadResponse(PosStruct):
    File: List[FileDTO] = None



class ApplicantDTO(BaseModel):
    EpguId: str = None
    Surname: str = None
    Name: str = None
    Patronymic: str = None
    Email: str = None
    Phone: str = None


class AttachmentIdsDTO(PosStruct):
    FileId: List[str] = None


class CustomFieldValueTypeModel(BaseModel):
    Name: str = None
    CustomFieldId: str = None
    FieldType: str = None


class CustomFieldValuesModel(PosStruct):
    CustomFieldValueType: List[CustomFieldValueTypeModel] = None


class OrganizationInfoModel(BaseModel):
    OrganizationPersonalAreaId: str = None
    Name: str = None
    Address: str = None
    Inn: str = None
    Kpp: str = None
    Ogrn: str = None
    Oktmo: str = None


class CreatedByDTO(BaseModel):
    Surname: str = None
    Name: str = None
    Patronymic: str = None


class RejectReasonDTO(BaseModel):
    Name: str = None


class AnswerAttachmentIdsDTO(PosStruct):
    FileId: List[str] = None


class AnswerDTO(BaseModel):
    AnswerType: str = None
    Comment: str = None
    RejectReason: RejectReasonDTO = None
    AttachmentIds: AnswerAttachmentIdsDTO = None


class StatusHistoriesModel(BaseModel):
    Status: str = None
    StatusText: str = None
    CreatedAt: str = None
    CreatedBy: CreatedByDTO = None
    Answer: AnswerDTO = None


class StatusHistoryModel(PosStruct):
    StatusHistories: List[StatusHistoriesModel] = None


class AppealDTO(PosStruct):
    Id: str = None
    PosId: str = None
    Applicant: ApplicantDTO = None
    Description: str = None
    AttachmentIds: AttachmentIdsDTO = None
    Location: str = None
    SubjectId: str = None
    SubsubjectId: str = None
    CustomFieldValues: CustomFieldValuesModel = None
    OrganizationPersonalAreaId: str = None
    OrganizationInfo: OrganizationInfoModel = None
    CreatedAt: str = None
    Status: str = None
    StatusText: str = None
    StatusHistory: StatusHistoryModel = None
    AnswerAt: str = None


class StatusDTO(BaseModel):
    OperationResult: str = None


class AppealResponse(PosStruct):
    Status: StatusDTO = None
    Appeal: AppealDTO = None


class FileDownloadResultModel(BaseModel):
    Status: StatusDTO = None
    File: FileDTO = None

class FileDownloadResponse(PosStruct):
    FileDownloadResult: List[FileDownloadResultModel] = None

class FSAttachmentModel(BaseModel):
    uuid: str = None
    UserName: str = None
    Password: str = None
    FileName: str = None

class FSAttachmentsList(PosStruct):
    FSAttachment: List[FSAttachmentModel] = None
