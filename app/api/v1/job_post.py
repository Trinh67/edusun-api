from fastapi import APIRouter, Depends, File, Form, Header, Request
from sqlalchemy.orm import Session

from app.dto.core import ExceptionResponseSchema
from app.dto.core.job_post import CreateJobPostRequestSchema, GetJobPostDetailResponseSchema, GetListJobPostsResponse, \
    GetListJobPostsRequest, UpdateJobPostRequestSchema, UpdateJobPostResponseSchema, CreateJobPostResponseSchema, \
    DeleteJobPostResponseSchema
from app.fastapi.dependencies import PermissionDependency, IsAuthenticated, IsAdmin
from app.helper.base_response import DataResponse, PagingDataResponse
from app.helper.db import db_session
from app.service.job_post import JobPostService

router = APIRouter()


@router.post(
    "",
    response_model=DataResponse[CreateJobPostResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
)
def create_job_post(
        db: Session = Depends(db_session), *,
        request: Request,
        req: CreateJobPostRequestSchema,
):
    job_post = JobPostService().create_job_post(db=db, req=req, user_id=request.user.id)
    return DataResponse().success_response(data=job_post)


@router.get(
    "/detail/{job_post_id}",
    response_model=DataResponse[GetJobPostDetailResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
def get_job_post_by_id(
        db: Session = Depends(db_session), *,
        request: Request,
        job_post_id: int,
):
    job_post = JobPostService().get_job_post_info(db=db, job_post_id=job_post_id, user_id=request.user.id)
    return DataResponse().success_response(data=job_post)


@router.get(
    "",
    response_model=PagingDataResponse[GetListJobPostsResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
def get_list_job_posts(
        db: Session = Depends(db_session), *,
        request: Request,
        req_query: GetListJobPostsRequest = Depends(GetListJobPostsRequest)
):
    job_posts, pagination = JobPostService().get_list_job_posts(db=db, req_query=req_query,
                                                                user_id=request.user.id)
    return PagingDataResponse().success(data=job_posts, pagination=pagination)


@router.put(
    "/{job_post_id}",
    response_model=DataResponse[UpdateJobPostResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
def update_job_post(
        db: Session = Depends(db_session), *,
        request: Request,
        job_post_id: int,
        req: UpdateJobPostRequestSchema,
):
    job_post = JobPostService().update_job_post(db=db, job_post_id=job_post_id, req=req, user_id=request.user.id)
    return DataResponse().success_response(data=job_post)


@router.delete(
    "/{job_post_id}",
    response_model=DataResponse[DeleteJobPostResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
def delete_job_post(
        db: Session = Depends(db_session), *,
        request: Request,
        job_post_id: int,
):
    job_post = JobPostService().delete_job_post(db=db, job_post_id=job_post_id, user_id=request.user.id)
    return DataResponse().success_response(data=job_post)
