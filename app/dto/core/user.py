from typing import List, Optional

from pydantic import Field, validator
from app.dto.base import CamelBaseModel
from app.dto.core import UpdateModel
from app.helper.custom_exception import InvalidFieldFormat
from app.helper.enum import UserStatus, UserType, UserRole, Gender
from app.helper.pagination import PaginationRequest, PaginationResponse
from app.helper.utils import is_phone_number_valid, is_valid_email


class LoginRequestSchema(CamelBaseModel):
    phone_or_email: str
    password: str


class LoginResponseSchema(CamelBaseModel):
    token: str


class UserDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    email: Optional[str]
    phone_number: Optional[str]
    fullname: Optional[str]
    avatar_url: Optional[str]
    status: Optional[UserStatus]
    type: Optional[UserType]
    role: Optional[UserRole]

    gender: Optional[Gender]
    age: Optional[int]
    birthday: Optional[str]
    address: Optional[str]


class UserInListResp(UserDTO):
    class Config:
        orm_mode = True

    id: int
    code: Optional[str]
    balance: Optional[int]


class GetListUsersResponse(PaginationResponse):
    users: List[UserInListResp]


class GetListUsersRequest(PaginationRequest):
    user_type: Optional[UserType]
    user_status: Optional[UserStatus]
    search: Optional[str]


class GetUserDetailResponseSchema(UserDTO):
    id: int
    code: Optional[str]
    balance: Optional[int]


class CreateUserRequestSchema(CamelBaseModel):
    email: str
    phone_number: str
    password: str = Field(..., min_length=6, max_length=32)
    fullname: str

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


class CreateUserResponseSchema(CamelBaseModel):
    id: int


class UpdateUserRequestSchema(UserDTO, UpdateModel):
    password: Optional[str] = Field(None, min_length=6, max_length=32)

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


class UpdateUserResponseSchema(CamelBaseModel):
    id: int


class DeleteUserResponseSchema(CamelBaseModel):
    pass
