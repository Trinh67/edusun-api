from sqlalchemy import Column, String, Text, SmallInteger, Integer
from app.model.base import BareBaseModel


class FileUpload(BareBaseModel):
    __tablename__ = 'file_upload'

    file_name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    create_by = Column(String(100))
