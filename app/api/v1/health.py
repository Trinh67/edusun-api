import logging
from fastapi import APIRouter
from app.helper.base_response import DataResponse

router = APIRouter()

_logger = logging.getLogger(__name__)


@router.get('/check', response_model=DataResponse)
def check_health():
    return DataResponse().success_response()

