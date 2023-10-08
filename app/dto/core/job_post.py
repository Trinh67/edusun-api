from typing import List, Optional

from pydantic import Field, validator
from app.dto.base import CamelBaseModel
from app.dto.core import UpdateModel
from app.helper.enum import PostType, PostStatus
from app.helper.pagination import PaginationRequest, PaginationResponse


class JobPostDTO(CamelBaseModel):
    class Config:
        orm_mode = True

    title: Optional[str]
    recruitment_object: Optional[str]
    description: Optional[str]
    benefit: Optional[str]
    other_information: Optional[str]
    bonus: Optional[int]
    currency: Optional[str]
    type: Optional[str]
    status: Optional[str]
    expired_at: Optional[str]


class JobPostInListResp(JobPostDTO):
    id: int


class GetListJobPostsResponse(PaginationResponse):
    job_posts: List[JobPostInListResp]


class GetListJobPostsRequest(PaginationRequest):
    type: Optional[PostType]
    status: Optional[PostStatus]
    search: Optional[str]


class GetJobPostDetailResponseSchema(JobPostDTO):
    id: int


class CreateJobPostRequestSchema(JobPostDTO):
    pass


class CreateJobPostResponseSchema(CamelBaseModel):
    id: int


class UpdateJobPostRequestSchema(JobPostDTO, UpdateModel):
    pass


class UpdateJobPostResponseSchema(CamelBaseModel):
    id: int


class DeleteJobPostResponseSchema(CamelBaseModel):
    pass
