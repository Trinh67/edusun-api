from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session

from app.dto.core.config import GetListSelectionValuesResponse, CreateSelectionValueRequestSchema, \
    CreateSelectionValueResponseSchema
from app.fastapi.dependencies import PermissionDependency, IsAdmin
from app.helper.base_response import DataResponse
from app.helper.db import db_session
from app.helper.enum import ConfigValueType
from app.service.config import ConfigService

router = APIRouter()


@router.get("",
            response_model=DataResponse[GetListSelectionValuesResponse],
            response_description="Success")
def get_configs(db: Session = Depends(db_session), *, types: List[ConfigValueType] = Query(default=[])):
    return DataResponse().success_response(data=ConfigService().get_list_selection_values(db=db,
                                                                                          value_types=types))


@router.post("", response_model=DataResponse[CreateSelectionValueResponseSchema],
             response_description="Success",
             dependencies=[Depends(PermissionDependency([IsAdmin]))])
async def create_config(db: Session = Depends(db_session), *, request: CreateSelectionValueRequestSchema):
    selection_value = ConfigService().create_selection_value(db, request)
    return DataResponse().success_response(data=selection_value)


@router.delete("/{config_id}", response_model=DataResponse[None],
               response_description="Success")
async def delete_config(db: Session = Depends(db_session), *,
                            config_id: int = Query(...)):
    ConfigService().delete_config(db, config_id)
    return DataResponse().success_response(data=None)
