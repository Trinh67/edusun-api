from fastapi import APIRouter, Depends, File, Form, Header, Request
from sqlalchemy.orm import Session

from app.dto.core import ExceptionResponseSchema
from app.dto.core.user import LoginResponseSchema, LoginRequestSchema, CreateUserRequestSchema, \
    GetUserDetailResponseSchema, GetListUsersResponse, GetListUsersRequest, UpdateUserRequestSchema, \
    UpdateUserResponseSchema, CreateUserResponseSchema
from app.fastapi.dependencies import PermissionDependency, IsAuthenticated, IsAdmin
from app.helper.base_response import DataResponse, PagingDataResponse
from app.helper.db import db_session
from app.service.user import UserService

router = APIRouter()


@router.post(
    "/login",
    response_model=DataResponse[LoginResponseSchema],
    responses={"404": {"model": ExceptionResponseSchema}},
)
def login(
        db: Session = Depends(db_session), *,
        request: LoginRequestSchema,
        user_agent: str = Header(default=None),
        real_ip: str = Header(None, alias='X-Real-IP')):
    token = UserService().login(db=db, req=request, user_agent=user_agent, ip=real_ip)
    return DataResponse().success_response(data={"token": token.token})


@router.post(
    "",
    response_model=DataResponse[CreateUserResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
)
def create_user(
        db: Session = Depends(db_session), *,
        request: CreateUserRequestSchema,
):
    user = UserService().create_user(db=db, req=request)
    return DataResponse().success_response(data=user)


@router.get(
    "/me",
    response_model=DataResponse[GetUserDetailResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
def get_user_info(
        db: Session = Depends(db_session), *,
        request: Request,
):
    user_id = request.user.id
    user = UserService().get_user_info(db=db, user_id=user_id)
    return DataResponse().success_response(data=user)


@router.get(
    "/detail/{user_id}",
    response_model=DataResponse[GetUserDetailResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
def get_user_by_id(
        db: Session = Depends(db_session), *,
        user_id: int,
):
    user = UserService().get_user_info(db=db, user_id=user_id)
    return DataResponse().success_response(data=user)


@router.get(
    "",
    response_model=PagingDataResponse[GetListUsersResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
def get_list_users(
        db: Session = Depends(db_session), *,
        request: Request,
        req_query: GetListUsersRequest = Depends(GetListUsersRequest)
):
    users, pagination = UserService().get_list_users(db=db, req_query=req_query, user_id=request.user.id)
    return PagingDataResponse().success(data=users, pagination=pagination)


@router.put(
    "/{user_id}",
    response_model=DataResponse[UpdateUserResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
def update_user(
        db: Session = Depends(db_session), *,
        user_id: int,
        request: UpdateUserRequestSchema,
):
    user = UserService().update_user(db=db, user_id=user_id, req=request)
    return DataResponse().success_response(data=user)
