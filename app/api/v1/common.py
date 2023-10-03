from fastapi import APIRouter, Depends, File, Form, Request
from sqlalchemy.orm import Session

from app.dto.core import ExceptionResponseSchema
from app.dto.core.common import UploadFileRequest
from app.fastapi.dependencies import PermissionDependency, IsAuthenticated
from app.helper.base_response import DataResponse
from app.helper.db import db_session
from app.helper.enum import UploadFileType
from app.service.common import CommonService
from setting import setting

router = APIRouter()


@router.post(
    "/upload-file",
    response_model=DataResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def upload_file(db: Session = Depends(db_session), *,
                      request: Request, file_type: UploadFileType,
                      upload_file_request: UploadFileRequest = File(...)):
    data = await CommonService.upload_file(db=db, user_id=request.user.id, file_type=file_type,
                                           file=upload_file_request,
                                           max_file_size=setting.DEFAULT_MAX_UPLOAD_SIZE)
    return DataResponse().success_response(data=data)
