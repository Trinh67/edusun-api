from datetime import datetime, timedelta

from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.dto.core.candidate import CreateCandidateRequestSchema, \
    CreateCandidateResponseSchema, GetCandidateDetailResponseSchema, GetListCandidatesResponse, UpdateCandidateRequestSchema, \
    UpdateCandidateResponseSchema
from app.helper.custom_exception import ObjectNotFound
from app.helper.enum import PostType, PostStatus, ObjectNotFoundType
from app.helper.pagination import Pagination
from app.model import Candidate


class CandidateService:
    @classmethod
    def create_candidate(
            cls, db: Session, req: CreateCandidateRequestSchema, user_id: int
    ) -> CreateCandidateResponseSchema:
        new_candidate = Candidate()
        for key, value in req.dict().items():
            setattr(new_candidate, key, value)
        new_candidate.created_by = user_id
        db.add(new_candidate)
        db.commit()
        db.refresh(new_candidate)

        return CreateCandidateResponseSchema(id=new_candidate.id)

    @classmethod
    def get_candidate_by_id(cls, db: Session, candidate_id: int, user_id: int) -> GetCandidateDetailResponseSchema:
        candidate = Candidate.first(db, Candidate.id == candidate_id)
        if not candidate:
            raise ObjectNotFound(obj=ObjectNotFoundType.CANDIDATE.value)

        return GetCandidateDetailResponseSchema.from_orm(candidate)

    @classmethod
    def get_list_candidates(cls, db: Session, req_query, user_id: int):
        query = Candidate.q(db)

        if req_query.status:
            query = query.filter(Candidate.status == req_query.status.value)

        if req_query.search:
            query = query.filter(or_(Candidate.fullname.ilike(f'%{req_query.search}%')))

        total_items = query.count()
        query = query.order_by(Candidate.created_at.desc())
        query = query.offset((req_query.page - 1) * req_query.page_size).limit(req_query.page_size)
        candidates = query.all()

        return GetListCandidatesResponse(candidates=[GetCandidateDetailResponseSchema.from_orm(u) for u in candidates]), \
               Pagination(current_page=req_query.page, page_size=req_query.page_size, total_items=total_items)

    @classmethod
    def update_candidate(cls, db: Session, candidate_id: int, req: UpdateCandidateRequestSchema, user_id: int):
        candidate = Candidate.first(db, Candidate.id == candidate_id)
        if not candidate:
            raise ObjectNotFound(obj=ObjectNotFoundType.CANDIDATE.value)

        for key, value in req.dict().items():
            setattr(candidate, key, value)

        candidate.updated_at = datetime.now()
        candidate.updated_by = user_id

        db.flush()
        db.commit()
        return UpdateCandidateResponseSchema(id=candidate.id)

    @classmethod
    def delete_candidate(cls, db: Session, candidate_id: int, user_id: int):
        candidate = Candidate.first(db, Candidate.id == candidate_id)
        if not candidate:
            raise ObjectNotFound(obj=ObjectNotFoundType.CANDIDATE.value)

        candidate.deleted_at = datetime.now()
        candidate.deleted_by = user_id
        db.flush()
        db.commit()
        return None
