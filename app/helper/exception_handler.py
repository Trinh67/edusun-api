from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.helper.base_response import DataResponse
from app.helper.custom_exception import CommonException, InternalServerError, request_get_message_validation


async def base_exception_handler(request, exc: CommonException):
    return JSONResponse(
        status_code=exc.http_code,
        content=jsonable_encoder(DataResponse().custom_response(exc.code, exc.message))
    )


async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(DataResponse().custom_response(exc.status_code, exc.detail))
    )


async def validation_exception_handler(request, exc):
    code, msg = request_get_message_validation(exc)
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(DataResponse().custom_response(code, msg))
    )


async def request_validation_exception_handler(request, exc):
    code, msg = request_get_message_validation(exc)
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(DataResponse().custom_response(code, msg))
    )


async def fastapi_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            DataResponse().custom_response(InternalServerError().code, InternalServerError().message)
        )
    )


