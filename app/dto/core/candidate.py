from datetime import datetime
from typing import List, Optional

from pydantic import validator

from app.dto.base import CamelBaseModel
from app.dto.core import UpdateModel
from app.helper.custom_exception import InvalidFieldFormat
from app.helper.enum import CandidateStatus, GraduationType
from app.helper.pagination import PaginationRequest, PaginationResponse
from app.helper.utils import is_phone_number_valid, is_valid_email


class CandidateDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    fullname: Optional[str]
    year_of_birth: Optional[int]
    address: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    average_graduation_score: Optional[float]
    parent_name: Optional[str]
    parent_phone_number: Optional[str]
    graduation_type: Optional[GraduationType]
    interested: Optional[str]
    note: Optional[str]
    attachment_url: Optional[str]
    contact_name: Optional[str]
    contact_phone_number: Optional[str]
    expected_admission: Optional[datetime]
    status: Optional[CandidateStatus]
    rejected_reason: Optional[str]
    failed_reason: Optional[str]


class CandidateInListResp(CandidateDTO):
    id: int


class GetListCandidatesResponse(PaginationResponse):
    candidates: List[CandidateInListResp]


class GetListCandidatesRequest(PaginationRequest):
    status: Optional[CandidateStatus]
    search: Optional[str]


class GetCandidateDetailResponseSchema(CandidateDTO):
    id: int


class CreateCandidateRequestSchema(CandidateDTO):
    pass

    @validator('phone_number')
    def validate_phone_number(cls, value):
        try:
            is_valid = is_phone_number_valid(value)
            if not is_valid:
                raise InvalidFieldFormat(field_name='phone_number')
            return value
        except Exception as e:
            raise InvalidFieldFormat(field_name='phone_number')

    @validator('email')
    def validate_email(cls, value):
        try:
            is_valid = is_valid_email(value)
            if not is_valid:
                raise InvalidFieldFormat(field_name='email')
            return value
        except Exception as e:
            raise InvalidFieldFormat(field_name='email')

    @validator('parent_phone_number')
    def validate_parent_phone_number(cls, value):
        try:
            is_valid = is_phone_number_valid(value)
            if not is_valid:
                raise InvalidFieldFormat(field_name='parent_phone_number')
            return value
        except Exception as e:
            raise InvalidFieldFormat(field_name='parent_phone_number')


class CreateCandidateResponseSchema(CamelBaseModel):
    id: int


class UpdateCandidateRequestSchema(CandidateDTO, UpdateModel):
    pass

    @validator('phone_number')
    def validate_phone_number(cls, value):
        try:
            is_valid = is_phone_number_valid(value)
            if not is_valid:
                raise InvalidFieldFormat(field_name='phone_number')
            return value
        except Exception as e:
            raise InvalidFieldFormat(field_name='phone_number')

    @validator('email')
    def validate_email(cls, value):
        try:
            is_valid = is_valid_email(value)
            if not is_valid:
                raise InvalidFieldFormat(field_name='email')
            return value
        except Exception as e:
            raise InvalidFieldFormat(field_name='email')

    @validator('parent_phone_number')
    def validate_parent_phone_number(cls, value):
        try:
            is_valid = is_phone_number_valid(value)
            if not is_valid:
                raise InvalidFieldFormat(field_name='parent_phone_number')
            return value
        except Exception as e:
            raise InvalidFieldFormat(field_name='parent_phone_number')


class UpdateCandidateResponseSchema(CamelBaseModel):
    id: int


class DeleteCandidateResponseSchema(CamelBaseModel):
    pass
