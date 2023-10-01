from sqlalchemy import Column, Unicode, TEXT, Integer, DateTime

from app.helper.enum import PostStatus, Currency, PostType
from app.model.base import BareBaseModel
from app.model.soft_modify_mixin import SoftModifyMixin


class JobPost(BareBaseModel, SoftModifyMixin):
    __tablename__ = "job_post"

    title = Column(Unicode(255), nullable=False)
    recruitment_object = Column(Unicode(255))
    description = Column(TEXT)
    benefit = Column(TEXT)
    other_information = Column(TEXT)
    bonus = Column(Integer)
    currency = Column(Unicode(255), nullable=False, default=Currency.VND.value)
    type = Column(Unicode(255), nullable=False, default=PostType.STUDY_ABROAD.value)
    status = Column(Unicode(32), nullable=False, default=PostStatus.DRAFT.value)
    expired_at = Column(DateTime)
