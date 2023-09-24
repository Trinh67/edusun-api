import json
import os
import io
import shutil
import logging
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd


from app.helper.custom_exception import CommonException, NotSupportFileType, FileTooLarge, FileEmpty, \
    InvalidFileFormat, ExistedFile
from app.helper.enum import ImportFileType
from app.helper.utils import generate_unique_filename
from app.model.file_upload import FileUpload
from setting import setting

_logger = logging.getLogger(__name__)

DATA_PATH = setting.DATA_STORAGE


class CommonService:
    @classmethod
    def import_customers(cls, db, file, max_file_size=setting.DEFAULT_MAX_UPLOAD_IMPORT_SIZE):
        try:
            file_type = ImportFileType.IMPORT_CUSTOMER.value
            filename = file.filename
            path = Path(filename)

            if path.suffix.lower() not in ['.xlsx']:
                raise NotSupportFileType()

            file_data = file.file.read()
            if len(file_data) > max_file_size * 1024 * 1024:
                raise FileTooLarge()
            if len(file_data) == 0:
                raise FileEmpty()

            # read file
            cols_to_use = []

            try:
                df = pd.read_excel(
                    io.BytesIO(file_data), usecols=cols_to_use,
                    dtype='string'
                )
            except Exception as e:
                _logger.error(e)
                raise InvalidFileFormat()

            # Change column name and convert data
            df = df.rename(columns={})
            df = df.replace({np.nan: ''})
            code_records = df.to_dict('records')
            # Todo: add data

            # save file and file_upload table
            file_name = cls.add_file_upload(db, file_type=file_type,
                                            filename=filename, file_data=file_data)
            db.commit()

            return None
        except CommonException as e:
            raise e
        except Exception as e:
            _logger.error(f"____error: {str(e)} when uploading file to storage.")
            raise e

    @classmethod
    def add_file_upload(cls, db, file_type, filename, file_data):
        # save file in local
        folder_path = f'{DATA_PATH}/{file_type}'
        is_folder_exist = os.path.exists(folder_path)
        if not is_folder_exist:
            os.makedirs(folder_path)

        file_name = generate_unique_filename(filename)
        file_path = f'{DATA_PATH}/{file_type}/{file_name}'
        is_file_exist = os.path.exists(file_path)
        if is_file_exist:
            raise ExistedFile()
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(BytesIO(file_data), buffer)

        # save file_upload table
        file_upload = FileUpload()
        file_upload.file_name = file_name
        file_upload.type = file_type
        db.add(file_upload)
        db.flush()

        return file_name
