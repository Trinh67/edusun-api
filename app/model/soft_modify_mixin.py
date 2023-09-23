from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr


class SoftModifyMixin:
    @declared_attr
    def created_by(self):
        return Column(Integer, nullable=True)

    @declared_attr
    def updated_by(self):
        return Column(Integer, nullable=True)

    @declared_attr
    def deleted_by(self):
        return Column(Integer, nullable=True)
