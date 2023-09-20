from typing import Optional
from pydantic import validator, BaseModel

from app.helper.custom_exception import InvalidField


class PaginationRequest(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = 10

    @validator('page')
    def validate_page(cls, v):
        if v <= 0:
            raise InvalidField('page')

        return v

    @validator('page_size')
    def validate_page_size(cls, v):
        if v <= 0:
            raise InvalidField('page_size')
        return v


class RequiredPaginationRequest(PaginationRequest):
    page: int
    page_size: int


class Pagination(BaseModel):
    current_page: int
    page_size: int
    total_items: int


class PaginationResponse(BaseModel):
    pagination: Optional[Pagination]


class KeysetPagination(BaseModel):
    offset: int = 0
    limit: int = 20
