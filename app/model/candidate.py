from sqlalchemy import Column, Unicode, SmallInteger, DateTime, Integer, Float

from app.helper.enum import UserStatus, UserRole, UserType, CandidateStatus
from app.model.base import BareBaseModel
from app.model.soft_modify_mixin import SoftModifyMixin


class Candidate(BareBaseModel, SoftModifyMixin):
    __tablename__ = "candidate"

    fullname = Column(Unicode(255), nullable=False)
    year_of_birth = Column(SmallInteger)
    address = Column(Unicode(255))
    phone_number = Column(Unicode(255))
    email = Column(Unicode(255))
    average_graduation_score = Column(Float)
    parent_name = Column(Unicode(255))
    parent_phone_number = Column(Unicode(255))
    graduation_type = Column(Unicode(255))
    interested = Column(Unicode(255))
    note = Column(Unicode(255))
    attachment_url = Column(Unicode(1024))
    contact_name = Column(Unicode(255))
    contact_phone_number = Column(Unicode(255))
    expected_admission = Column(DateTime)
    status = Column(Unicode(32), nullable=False, default=CandidateStatus.WAITTING.value)
    rejected_reason = Column(Unicode(255))
    failed_reason = Column(Unicode(255))
