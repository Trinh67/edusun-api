import typing
from pathlib import Path
from typing import Type, Any, Union

from fastapi import UploadFile as UploadFileSource
from starlette.datastructures import UploadFile as StarletteUploadFile

from app.helper.custom_exception import RequiredFile, NotSupportFileType


class UploadFileRequest(UploadFileSource):
    file: typing.IO
    filename: str
    file_data = Union[bytes, str]

    @classmethod
    def validate(cls: Type['UploadFileRequest'], v: Any) -> Any:
        if not isinstance(v, StarletteUploadFile) or not v.file or not v.filename:
            raise RequiredFile()
        path = Path(v.filename)
        if not path.name or path.suffix.lower() not in ['.csv', '.xls', '.xlsx', '.pdf', '.txt', '.docs', '.doc',
                                                        '.docx', '.pptx', '.jpg', '.png', 'jpeg']:
            raise NotSupportFileType()

        return v
