from typing import Optional, List, Union
from humps import camelize, pascalize
from pydantic import BaseModel


class OpenApiResponseModel:
    http_code: str
    description: str
    code: int
    message: str
    data: Optional[dict]

    def __init__(self, http_code: str, description: str, code: int, message: str,
                 data: Optional[Union[dict, List]] = None):
        self.http_code = http_code
        self.description = description
        self.code = code
        self.message = message
        self.data = data


class CamelBaseModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


