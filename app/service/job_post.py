from datetime import datetime, timedelta

from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.dto.core.job_post import CreateJobPostRequestSchema, \
    CreateJobPostResponseSchema, GetJobPostDetailResponseSchema, GetListJobPostsResponse, UpdateJobPostRequestSchema, \
    UpdateJobPostResponseSchema
from app.helper.custom_exception import ObjectNotFound
from app.helper.enum import PostType, PostStatus, ObjectNotFoundType
from app.helper.pagination import Pagination
from app.model import JobPost


class JobPostService:
    @classmethod
    def create_job_post(
            cls, db: Session, req: CreateJobPostRequestSchema, user_id: int
    ) -> CreateJobPostResponseSchema:
        new_job_post = JobPost()
        for key, value in req.dict().items():
            setattr(new_job_post, key, value)
        new_job_post.created_by = user_id
        db.add(new_job_post)
        db.commit()
        db.refresh(new_job_post)

        return CreateJobPostResponseSchema(id=new_job_post.id)

    @classmethod
    def get_job_post_by_id(cls, db: Session, job_post_id: int, user_id: int) -> GetJobPostDetailResponseSchema:
        job_post = JobPost.first(db, JobPost.id == job_post_id)
        if not job_post:
            raise ObjectNotFound(obj=ObjectNotFoundType.JOB_POST.value)

        return GetJobPostDetailResponseSchema.from_orm(job_post)

    @classmethod
    def get_list_job_posts(cls, db: Session, req_query, user_id: int):
        query = JobPost.q(db)

        if req_query.type:
            query = query.filter(JobPost.type == req_query.job_post_type.value)

        if req_query.status:
            query = query.filter(JobPost.status == req_query.job_post_status.value)

        if req_query.search:
            query = query.filter(or_(JobPost.title.ilike(f'%{req_query.search}%')))

        total_items = query.count()
        query = query.order_by(JobPost.created_at.desc())
        query = query.offset((req_query.page - 1) * req_query.page_size).limit(req_query.page_size)
        job_posts = query.all()

        return GetListJobPostsResponse(job_posts=[GetJobPostDetailResponseSchema.from_orm(u) for u in job_posts]), \
               Pagination(current_page=req_query.page, page_size=req_query.page_size, total_items=total_items)

    @classmethod
    def update_job_post(cls, db: Session, job_post_id: int, req: UpdateJobPostRequestSchema, user_id: int):
        job_post = JobPost.first(db, JobPost.id == job_post_id)
        if not job_post:
            raise ObjectNotFound(obj=ObjectNotFoundType.JOB_POST.value)

        for key, value in req.dict().items():
            setattr(job_post, key, value)

        job_post.updated_by = user_id
        job_post.updated_at = datetime.now()

        db.flush()
        db.commit()
        return UpdateJobPostResponseSchema(id=job_post.id)

    @classmethod
    def delete_job_post(cls, db: Session, job_post_id: int, user_id: int):
        job_post = JobPost.first(db, JobPost.id == job_post_id)
        if not job_post:
            raise ObjectNotFound(obj=ObjectNotFoundType.JOB_POST.value)

        job_post.deleted_at = datetime.now()
        job_post.deleted_by = user_id
        db.flush()
        db.commit()
        return None
