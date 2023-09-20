from fastapi import APIRouter, Depends, File, Form
from sqlalchemy.orm import Session

from app.dto.core import ExceptionResponseSchema
from app.dto.core.common import UploadFileRequest
from app.helper.base_response import DataResponse
from app.helper.db import db_session
from app.service.common import CommonService
from setting import setting

router = APIRouter()


@router.post(
    "/import-customers",
    response_model=DataResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
def import_codes(db: Session = Depends(db_session), *,
                 upload_file_request: UploadFileRequest = File(...)):
    data = CommonService().import_customers(db, file=upload_file_request,
                                            max_file_size=setting.DEFAULT_MAX_UPLOAD_IMPORT_SIZE)
    return DataResponse().success_response(data=data)
