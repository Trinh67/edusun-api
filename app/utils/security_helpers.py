import base64
from datetime import datetime, timedelta
from typing import Any, Union
from cryptography.fernet import Fernet
from passlib.context import CryptContext

from core.config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fernet = Fernet(config.ENCRYPT_KEY.encode())

# ALGORITHM = "HS256"


# def create_access_token(
#     subject: Union[str, Any], expires_delta: timedelta = None
# ) -> str:
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(
#             minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#         )
#     to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# def create_refresh_token(
#     subject: Union[str, Any], expires_delta: timedelta = None
# ) -> str:
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(
#             minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
#         )
#     to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def encrypt_data(data: str) -> str:
    data = fernet.encrypt(data.encode())
    return data.decode()


def decrypt_data(variable: str) -> str:
    return fernet.decrypt(variable.encode()).decode()
