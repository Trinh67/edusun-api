from sqlalchemy import Column, Unicode, SmallInteger, DateTime, Integer

from app.helper.enum import UserStatus, UserRole, UserType
from app.model.base import BareBaseModel
from app.model.soft_modify_mixin import SoftModifyMixin


class User(BareBaseModel, SoftModifyMixin):
    __tablename__ = "user"

    email = Column(Unicode(255), nullable=False, unique=True)
    phone = Column(Unicode(255), nullable=False, unique=True)
    password = Column(Unicode(255), nullable=False)
    password_hash = Column(Unicode(255), nullable=True)
    password_reset = Column(Unicode(255), nullable=True)
    password_reset_hash = Column(Unicode(255), nullable=True)
    fullname = Column(Unicode(255), nullable=False)
    avatar_url = Column(Unicode(1024))
    status = Column(Unicode(32), nullable=False, default=UserStatus.ACTIVE.value)
    type = Column(Unicode(32), nullable=False, default=UserType.COLLABORATOR.value)
    role = Column(Unicode(32), nullable=True)
    code = Column(Unicode(255), nullable=False, unique=True)
    balance = Column(Integer, nullable=False, default=0)

    # indentify
    gender = Column(Unicode(32))
    age = Column(SmallInteger)
    birthday = Column(DateTime)
    address = Column(Unicode(255))
