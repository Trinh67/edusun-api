from typing import Optional, Tuple

from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from app.services.user import UserService
from ..schemas import CurrentUser


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()
        access_token: str = conn.headers.get("Access-Token")

        if not access_token:
            return False, current_user

        user_id = await UserService().get_user_id_by_token(access_token)

        # print("user_id", user_id)

        current_user.id = user_id
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
