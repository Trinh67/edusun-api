from typing import List, Optional

from app.dto.base import CamelBaseModel
from app.helper.enum import UserStatus, UserType, UserRole


class LoginRequestSchema(CamelBaseModel):
    email: Optional[str]
    username: Optional[str]
    password: str


class LoginResponseSchema(CamelBaseModel):
    token: str


class UserDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    email: Optional[str]
    username: Optional[str]
    fullname: Optional[str]
    avatar_url: Optional[str]
    status: Optional[UserStatus]
    type: Optional[UserType]
    role: Optional[UserRole]


class UserInListResp(UserDTO):
    class Config:
        orm_mode = True

    id: int


class GetListUsersResponse(CamelBaseModel):
    users: List[UserInListResp]


class GetListUsersRequest(CamelBaseModel):
    user_type: Optional[UserType]
    user_status: Optional[UserStatus]
    search: Optional[str]


class GetUserDetailResponseSchema(UserDTO):
    id: int


class CreateUserRequestSchema(UserDTO):
    username: str
    password: str


class CreateUserResponseSchema(CamelBaseModel):
    id: int


class UpdateUserRequestSchema(CamelBaseModel):
    id: int
    password: Optional[str]
    email: Optional[str]
    fullname: Optional[str]
    avatar_url: Optional[str]
    status: Optional[UserStatus]
    type: Optional[UserType]
    role: Optional[UserRole]


class UpdateUserResponseSchema(CamelBaseModel):
    id: int


class DeleteUserResponseSchema(CamelBaseModel):
    pass
