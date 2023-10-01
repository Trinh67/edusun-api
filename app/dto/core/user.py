from typing import List, Optional

from pydantic import Field
from app.dto.base import CamelBaseModel
from app.dto.core import UpdateModel
from app.helper.enum import UserStatus, UserType, UserRole, Gender
from app.helper.pagination import PaginationRequest, PaginationResponse


class LoginRequestSchema(CamelBaseModel):
    email: Optional[str]
    phone: Optional[str]
    password: str


class LoginResponseSchema(CamelBaseModel):
    token: str


class UserDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    email: Optional[str]
    phone: Optional[str]
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
    phone: str
    password: str = Field(..., min_length=6, max_length=32)
    fullname: str


class CreateUserResponseSchema(CamelBaseModel):
    id: int


class UpdateUserRequestSchema(UserDTO, UpdateModel):
    password: Optional[str] = Field(None, min_length=6, max_length=32)


class UpdateUserResponseSchema(CamelBaseModel):
    id: int


class DeleteUserResponseSchema(CamelBaseModel):
    pass
