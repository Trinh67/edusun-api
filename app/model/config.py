from sqlalchemy import Column, Unicode, SmallInteger

from app.model.base import BareBaseModel


class Config(BareBaseModel):
    __tablename__ = "config"

    name = Column(Unicode(255))
    type = Column(Unicode(255))
    value = Column(Unicode(255))
