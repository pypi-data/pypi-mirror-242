from typing import List, Optional, Any

from pydantic import BaseModel, validator, Field
from rest_framework.exceptions import ValidationError

from modules.core.models.permissions.sub_permissions import UserStatus


class VotingPermissionsDto(BaseModel):
    allowed_localities_ids: Optional[List[int]]
    allowed_categories_ids: Optional[List[int]]


class InitiativesPermissionsDto(BaseModel):
    allowed_localities_ids: Optional[List[int]]
    allowed_categories_ids: Optional[List[int]]


class MapWorksPermissionsDto(BaseModel):
    allowed_localities_ids: Optional[List[int]]
    allowed_categories_ids: Optional[List[int]]


class PlansPermissionsDto(BaseModel):
    allowed_localities_ids: Optional[List[int]]
    allowed_categories_ids: Optional[List[int]]


class OperatorPermissionsCreateDto(BaseModel):
    modules_permissions: List[str]
    department_id: int

    appeals_categories: List[int]
    appeals_localities: List[int]
    appeals_switch: bool

    encouragement_categories: List[int]
    encouragement_localities: List[int]
    encouragement_switch: bool

    initiative_categories: List[int]
    initiative_localities: List[int]
    initiative_subcategories: List[int]
    initiative_switch: bool

    suggestion_categories: List[int]
    suggestion_localities: List[int]
    suggestion_switch: bool

    voting_categories: List[int]
    voting_localities: List[int]
    voting_switch: bool

    map_works_categories: List[int]
    map_works_localities: List[int]
    map_works_switch: bool

    plans_categories: List[int]
    plans_localities: List[int]
    plans_switch: bool

    voting_permissions: Optional[VotingPermissionsDto]
    initiative_permissions: Optional[InitiativesPermissionsDto]
    map_works_permissions: Optional[MapWorksPermissionsDto]
    plans_permissions: Optional[PlansPermissionsDto]


class CuratorPermissionsCreateDto(BaseModel):
    modules_permissions: List[str]
    department_id: int
    voting_permissions: Optional[VotingPermissionsDto]
    initiative_permissions: Optional[InitiativesPermissionsDto]
    map_works_permissions: Optional[MapWorksPermissionsDto]
    plans_permissions: Optional[PlansPermissionsDto]


class AdminLkoPermissionsCreateDto(BaseModel):
    department_id: int


class UserSubPermissionsCreateDto(BaseModel):
    operator_permissions: Optional[OperatorPermissionsCreateDto]
    admin_lko_permissions: Optional[AdminLkoPermissionsCreateDto]
    curator_permissions: Optional[List[CuratorPermissionsCreateDto]]
    roles: List[str]
    status: str = Field(default=UserStatus.IS_ACTIVE)
    email: str = None
    position: str
    sub_phone: Optional[str]

    @validator("status")
    def validate_status(cls, value):
        if value not in UserStatus.RESOLVER.keys():
            raise ValidationError("Неккоректный статус")
        return value

