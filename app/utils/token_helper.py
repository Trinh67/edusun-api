from datetime import datetime, timedelta

import jwt

from app import CommonException
from setting import setting


class TokenHelper:
    @staticmethod
    def encode(payload: dict, expire_period: int = 3600) -> str:
        token = jwt.encode(
            payload={
                **payload,
                "exp": datetime.utcnow() + timedelta(seconds=expire_period),
            },
            key=setting.JWT_SECRET_KEY,
            algorithm=setting.JWT_ALGORITHM,
        )
        return token

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                setting.JWT_SECRET_KEY,
                setting.JWT_ALGORITHM,
            )
        except jwt.exceptions.DecodeError:
            raise CommonException(http_code=400, message="Invalid token")
        except jwt.exceptions.ExpiredSignatureError:
            raise CommonException(http_code=400, message="Expired token")

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                setting.JWT_SECRET_KEY,
                setting.JWT_ALGORITHM,
                options={"verify_exp": False},
            )
        except jwt.exceptions.DecodeError:
            raise CommonException(http_code=400, message="Invalid token")
