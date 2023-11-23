from typing import List, Optional

from pydantic import BaseModel, Field


class DepartmentPermissionsCreateDto(BaseModel):
    modules_permissions: Optional[List[str]]
    voting_categories_ids: Optional[List[int]] = Field(alias="voting_categories")
    initiative_categories_ids: Optional[List[int]] = Field(alias="initiative_categories")
    map_works_categories_ids: Optional[List[int]] = Field(alias="map_works_categories")
    plans_categories_ids: Optional[List[int]] = Field(alias="plans_categories")
    appeals_categories_ids: Optional[List[int]] = Field(alias="appeals_categories")
    encouragement_categories_ids: Optional[List[int]] = Field(alias="encouragement_categories")
    suggestion_categories_ids: Optional[List[int]] = Field(alias="suggestion_categories")
