from typing import List, Optional

from app.dto.base import CamelBaseModel
from app.helper.enum import ConfigValueType


class SelectionValueDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    id: int
    value: str
    name: str


class InListSelectionValueDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    id: int
    value: str


class SelectionInListSelection(CamelBaseModel):
    value_type: Optional[str]
    values: Optional[List[InListSelectionValueDTO]]


class GetListSelectionValuesResponse(CamelBaseModel):
    configs: Optional[List[SelectionInListSelection]]


class CreateSelectionValueRequestSchema(CamelBaseModel):
    value: str
    name: str
    type: ConfigValueType


class CreateSelectionValueResponseSchema(CamelBaseModel):
    config_id: int
