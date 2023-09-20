from typing import Optional, Generic, TypeVar, Union
from pydantic.generics import GenericModel
from app.helper.pagination import PaginationResponse, Pagination, KeysetPagination

T = TypeVar("T")


class DataResponse(GenericModel, Generic[T]):
    code: int = ""
    message: str = ""
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: int, message: str, data: T = None):
        self.code = code
        self.message = message
        self.data = data
        return self

    def success_response(self, data: T = None):
        self.code = 200
        self.message = 'Success'
        self.data = data
        return self


class PagingDataResponse(GenericModel, Generic[T]):
    code: int = 200
    message: str = ""
    data: Optional[T] = None

    def success(self, data: PaginationResponse, pagination: Union[Pagination, KeysetPagination]):
        self.code = 200
        self.message = "Success"
        self.data = data
        self.data.pagination = pagination
        return self
