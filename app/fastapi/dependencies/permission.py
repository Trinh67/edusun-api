from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

from app.service.user import UserService

from app.helper.custom_exception import UnauthorizedException, ForbiddenException, CommonException


class BasePermission(ABC):
    exception = CommonException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException(message="Token is invalid or expired.")

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class IsAdmin(BasePermission):
    exception = UnauthorizedException(message="Token is invalid or expired.")

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        is_admin = UserService().is_admin(user_id=user_id)
        if not is_admin:
            raise ForbiddenException(message="You are not permission to access this resource.")
        return is_admin


class IsSuperAdmin(BasePermission):
    exception = UnauthorizedException(message="Token is invalid or expired.")

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        is_super_admin = UserService().is_super_admin(user_id=user_id)
        if not is_super_admin:
            raise ForbiddenException(message="You are not permission to access this resource.")
        return is_super_admin


class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[Type[BasePermission]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Access-Token")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise cls.exception
