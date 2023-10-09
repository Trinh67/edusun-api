from fastapi import APIRouter, Depends, File, Form, Header, Request
from sqlalchemy.orm import Session

from app.dto.core import ExceptionResponseSchema
from app.dto.core.candidate import CreateCandidateRequestSchema, GetCandidateDetailResponseSchema, \
    GetListCandidatesResponse, GetListCandidatesRequest, UpdateCandidateRequestSchema, UpdateCandidateResponseSchema, \
    CreateCandidateResponseSchema, DeleteCandidateResponseSchema
from app.fastapi.dependencies import PermissionDependency, IsAuthenticated, IsAdmin
from app.helper.base_response import DataResponse, PagingDataResponse
from app.helper.db import db_session
from app.service.candidate import CandidateService

router = APIRouter()


@router.post(
    "",
    response_model=DataResponse[CreateCandidateResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
def create_candidate(
        db: Session = Depends(db_session), *,
        request: Request,
        req: CreateCandidateRequestSchema,
):
    candidate = CandidateService().create_candidate(db=db, req=req, user_id=request.user.id)
    return DataResponse().success_response(data=candidate)


@router.get(
    "/detail/{candidate_id}",
    response_model=DataResponse[GetCandidateDetailResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
def get_candidate_by_id(
        db: Session = Depends(db_session), *,
        request: Request,
        candidate_id: int,
):
    candidate = CandidateService().get_candidate_by_id(db=db, candidate_id=candidate_id, user_id=request.user.id)
    return DataResponse().success_response(data=candidate)


@router.get(
    "",
    response_model=PagingDataResponse[GetListCandidatesResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
def get_list_candidates(
        db: Session = Depends(db_session), *,
        request: Request,
        req_query: GetListCandidatesRequest = Depends(GetListCandidatesRequest)
):
    candidates, pagination = CandidateService().get_list_candidates(db=db, req_query=req_query,
                                                                user_id=request.user.id)
    return PagingDataResponse().success(data=candidates, pagination=pagination)


@router.put(
    "/{candidate_id}",
    response_model=DataResponse[UpdateCandidateResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
def update_candidate(
        db: Session = Depends(db_session), *,
        request: Request,
        candidate_id: int,
        req: UpdateCandidateRequestSchema,
):
    candidate = CandidateService().update_candidate(db=db, candidate_id=candidate_id, req=req, user_id=request.user.id)
    return DataResponse().success_response(data=candidate)


@router.delete(
    "/{candidate_id}",
    response_model=DataResponse[DeleteCandidateResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
def delete_candidate(
        db: Session = Depends(db_session), *,
        request: Request,
        candidate_id: int,
):
    candidate = CandidateService().delete_candidate(db=db, candidate_id=candidate_id, user_id=request.user.id)
    return DataResponse().success_response(data=candidate)
