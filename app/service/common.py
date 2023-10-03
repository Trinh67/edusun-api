import json
import os
import io
import shutil
import logging
from io import BytesIO
from pathlib import Path
from sqlalchemy.orm import Session

import numpy as np
import pandas as pd

from app.adapter.firebase import FirebaseService
from app.helper.custom_exception import CommonException, NotSupportFileType, FileTooLarge, FileEmpty, \
    InvalidFileFormat, ExistedFile, ValidateException
from app.helper.enum import ImportFileType, UploadFileType
from app.helper.utils import generate_unique_filename
from app.model.file_upload import FileUpload
from setting import setting

_logger = logging.getLogger(__name__)

DATA_PATH = setting.DATA_STORAGE


class CommonService:
    @classmethod
    async def upload_file(cls, db: Session, file_type: UploadFileType, user_id, file,
                          max_file_size=setting.DEFAULT_MAX_UPLOAD_SIZE) -> dict:
        try:
            filename = file.filename
            path = Path(filename)

            if file_type.value:
                if file_type.value == UploadFileType.IMAGE.value:
                    if path.suffix.lower() not in ['.jpg', '.png', '.jpeg']:
                        raise ValidateException(415, 'File type is not supported image type')
                if file_type.value == UploadFileType.ATTACHMENT.value:
                    if path.suffix.lower() not in ['.csv', '.xls', '.xlsx', '.pdf', '.txt', '.docs', '.doc',
                                                   '.docx', '.pptx', '.jpg', '.png', 'jpeg']:
                        raise ValidateException(415, 'File type is not supported attachment type')

            file_data = file.file.read()
            if len(file_data) > max_file_size * 1024 * 1024:
                raise ValidateException(413, 'File is too large')
            if len(file_data) == 0:
                raise ValidateException(410, 'File is empty')

            # save file and file_upload table
            file_name = cls.add_file_upload(db, user_id, file_type.value, filename)
            db.commit()

            # Upload file to firebase
            file_url = f"{file_type.value}/{file_name}"
            FirebaseService().upload_file(file_name=file_url, file_data=file_data)

            return {'url': f"{file_url}"}
        except CommonException as e:
            raise e
        except Exception as e:
            _logger.error(f"____error: {str(e)} when uploading file to storage.")
            raise e

    @classmethod
    def add_file_upload(cls, db, user_id, file_type, filename):
        file_name = generate_unique_filename(filename)
        # save file_upload table
        file_upload = FileUpload()
        file_upload.file_name = file_name
        file_upload.type = file_type
        file_upload.create_by = user_id
        db.add(file_upload)
        db.flush()

        return file_name
