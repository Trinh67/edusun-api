from sqlalchemy import Column, Unicode, SmallInteger, DateTime

from app.helper.enum import UserStatus, UserRole, UserType
from app.model.base import BareBaseModel
from app.model.soft_modify_mixin import SoftModifyMixin


class User(BareBaseModel, SoftModifyMixin):
    __tablename__ = "user"

    email = Column(Unicode(255))
    username = Column(Unicode(255), nullable=False, unique=True)
    password_hash = Column(Unicode(255), nullable=True)
    password_encrypted = Column(Unicode(255), nullable=True)
    password_reset_hash = Column(Unicode(255), nullable=True)
    password_reset_encrypted = Column(Unicode(255), nullable=True)
    fullname = Column(Unicode(255))
    avatar_url = Column(Unicode(1024))
    status = Column(Unicode(32), nullable=False, default=UserStatus.ACTIVE.value)
    type = Column(Unicode(32), nullable=False, default=UserType.STUDENT.value)
    role = Column(Unicode(32), nullable=True, default=UserRole.NONE.value)

    # indentify
    gender = Column(Unicode(32))
    age = Column(SmallInteger)
    birthday = Column(DateTime)
    phone = Column(Unicode(255))
    address = Column(Unicode(255))
