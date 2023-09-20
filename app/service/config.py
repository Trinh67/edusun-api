import logging
from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from app.dto.core.config import GetListSelectionValuesResponse, CreateSelectionValueResponseSchema, \
    CreateSelectionValueRequestSchema
from app.helper.custom_exception import ExistedObject, ObjectNotFound
from app.helper.enum import ObjectNotFoundType
from app.model.config import Config

_logger = logging.getLogger(__name__)


class ConfigService:
    @classmethod
    def get_list_selection_values(
            cls,
            db: Session,
            value_types: Optional[List[str]] = None
    ) -> GetListSelectionValuesResponse:
        configs = Config.q(db).filter(Config.type.in_([v for v in value_types])).all()

        selections = []

        for type_config in value_types:
            selections.append({
                'value_type': type_config,
                'values': [{'id': c.id, 'value': c.name} for c in configs if c.type == type_config]
            })

        response = GetListSelectionValuesResponse()
        response.configs = selections
        return response

    @classmethod
    def create_selection_value(
            cls, db, req: CreateSelectionValueRequestSchema
    ) -> CreateSelectionValueResponseSchema:
        # Check duplicate value in same type
        selection_value = Config.first(db, Config.type == req.type.value, Config.name == req.name,
                                       Config.deleted_at.is_(None))

        if selection_value:
            raise ExistedObject("ConfigName")

        selection_value = Config.create(db, data=req.dict())
        db.flush()
        db.commit()

        return CreateSelectionValueResponseSchema(config_id=selection_value.id)

    @classmethod
    def delete_config(cls, db: Session, config_id: int):
        config = Config.first(db, Config.id == config_id, Config.deleted_at.is_(None))
        if not config:
            raise ObjectNotFound(ObjectNotFoundType.CONFIG.value)

        config.deleted_at = datetime.now()
        db.flush()
        db.commit()
        return None
