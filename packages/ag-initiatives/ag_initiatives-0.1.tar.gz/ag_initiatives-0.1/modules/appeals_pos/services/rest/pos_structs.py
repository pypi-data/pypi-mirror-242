import logging
from typing import Optional, Union, List

from pydantic import BaseModel

from config.settings import settings

logger = logging.getLogger("structs")


class PosStruct(BaseModel):
    def to_dict(self) -> dict:
        return self.dict()

    @classmethod
    def from_dict(cls, data: Union[dict, list, None]):
        return cls.parse_obj(data)

    def to_xml(self):
        pass


class AuthDataStruct(PosStruct):
    """Структура тела POST запроса для получения токена"""

    username: str
    password: str
    scope: str
    grant_type: str


class AuthResponseStruct(PosStruct):
    """Структура ответа на получение токена"""

    access_token: str
    token_type: str
    expires_in: int
    scope: str
    patronymic: str
    system: bool
    surname: str
    name: str
    rsId: Optional[int] = None
    userId: int
    email: str
    superUser: Optional[bool] = None
    jti: str


class RegionResponseStruct(PosStruct):
    """Структура ответа на получение регионов региона (GET /regions)"""

    id: int
    name: str
    okato: int
    coordinates: str


class SubjectResponseStruct(PosStruct):
    """Структура ответа на получение категорий (GET /subjects/regions/24/all)"""

    id: int
    name: str


class SubSubjectResponseStruct(PosStruct):
    """Структура ответа на получение подкатегорий категории (GET /subsubjects/subject/{subject_id}/region/24/)"""

    id: int
    name: str
    subject: SubjectResponseStruct


class HistoryAnswerRejectReasonStruct(PosStruct):
    """Структура, вложенная в HistoryAnswerStruct"""

    id: int
    name: str


class HistoryCreatedByStruct(PosStruct):
    """Структура, вложенная в HistoryStruct"""

    surname: str
    name: str
    patronymic: str
    position: Optional[str]
    email: Optional[str]
    phone: Optional[str]


class HistoryAnswerStruct(PosStruct):
    """Структура, вложенная в HistoryStruct"""

    answer_type: str
    comment: Optional[str]
    reject_reason: Optional[HistoryAnswerRejectReasonStruct]

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None
        reject_reason_dict = data.pop("rejectReason", None)
        reject_reason = (
            HistoryAnswerRejectReasonStruct.from_dict(reject_reason_dict)
            if reject_reason_dict
            else None
        )
        return cls(
            answer_type=data.get("answerType"),
            comment=data.get("comment", None),
            reject_reason=reject_reason,
        )


class HistoryStruct(PosStruct):
    """Структура, вложенная в AppealResponseStruct"""

    status: str
    status_text: str
    answer: Optional[HistoryAnswerStruct]
    created_at: str
    created_by: Optional[HistoryCreatedByStruct]

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None
        answer = HistoryAnswerStruct.from_dict(data.pop("answer", None))
        created_by_data = data.pop("createdBy", None)
        created_by = HistoryCreatedByStruct.from_dict(created_by_data) if created_by_data else None
        return cls(
            status=data.get("status"),
            status_text=data.get("statusText"),
            answer=answer,
            created_at=data.get("createdAt"),
            created_by=created_by,
        )


class AppealResponseStruct(PosStruct):
    """Структура на получение статуса обращения и обновления данных по нему
    (GET appeal-service/external-appeal-system/appeals/563006508)"""

    pos_id: int
    status: str
    status_text: str
    history: Optional[List[HistoryStruct]]

    @classmethod
    def from_dict(cls, data: Union[dict, list, None]):
        if not data:
            return None

        history: List[HistoryStruct] = list()
        history_dict = data.get("history", None)
        logger.debug(history_dict)
        if history_dict:
            for history_object in history_dict:
                history.append(HistoryStruct.from_dict(history_object))

        return cls(
            pos_id=data.get("posId"),
            status=data.get("status"),
            status_text=data.get("statusText"),
            history=history,
        )


class OrganizationInfoStruct(PosStruct):
    ogrn: str = "1022402674744"


class ApplicantDataStruct(PosStruct):
    epguId: int
    name: str
    email: str
    surname: Optional[str]
    patronymic: Optional[str]
    phone: Optional[str]


class AppealDataStruct(PosStruct):
    description: str
    createdAt: str
    applicant: ApplicantDataStruct
    subjectId: Optional[int]
    subsubjectId: Optional[int]
    attachmentIds: Optional[List[str]]
    location: Optional[str]
    organizationInfo: OrganizationInfoStruct = OrganizationInfoStruct()
    regionId: int = settings.REGION_ID
