from sqlalchemy import Column, Unicode, SmallInteger, BigInteger, DateTime

from app.model.base import BareBaseModel


class UserToken(BareBaseModel):
    __tablename__ = "user_token"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    token = Column(Unicode(255), nullable=False)
    expired_at = Column(DateTime, nullable=False)
    ip_address = Column(Unicode(128))
    user_agent = Column(Unicode(1024))

