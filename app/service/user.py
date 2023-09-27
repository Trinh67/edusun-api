import secrets
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.dto.core.user import LoginRequestSchema, LoginResponseSchema
from app.helper.custom_exception import FieldIsRequired, UnauthorizedException
from app.helper.enum import UserType, UserRole, UserStatus
from app.model import User, UserToken
from app.helper.db import db_session
from app.utils.security_helpers import verify_password
from setting import setting


class UserService:
    @classmethod
    def get_user_id_by_token(cls, db: Session = db_session, token: str = None) -> Optional[int]:
        user_token = UserToken.q(db).filter(UserToken.token == token)

        if not user_token:
            # raise here return HTTP 500 error??
            # raise HTTPException(status_code=403, detail="Invalid Token")
            return None

        if user_token.expired_at < datetime.utcnow():
            # raise HTTPException(status_code=403, detail="Token expired")
            return None

        # TODO: check user status
        user = User.q(db).filter(User.id == user_token.user_id, User.deleted_at.is_(None)).first()
        if not user or user.status != UserStatus.ACTIVE.value:
            # raise HTTPException(status_code=403, detail="User not found or blocked")
            return None

        return user_token.user_id

    @classmethod
    def is_admin(cls, db: Session = db_session, user_id: int = None) -> bool:
        user = User.q(db).filter(User.id == user_id, User.deleted_at.is_(None))
        if not user:
            return False

        if user.type != UserType.STAFF.value:
            return False

        if user.role not in [UserRole.ADMIN.value, UserRole.SUPER_ADMIN.value]:
            return False

        return True

    @classmethod
    def is_super_admin(cls, db: Session = db_session, user_id: int = None) -> bool:
        user = User.q(db).filter(User.id == user_id, User.deleted_at.is_(None))
        if not user:
            return False

        if user.type != UserType.STAFF.value:
            return False

        if user.role not in [UserRole.SUPER_ADMIN.value]:
            return False

        return True

    @classmethod
    def login(cls, db: Session, req: LoginRequestSchema, user_agent: str, ip: str) -> LoginResponseSchema:
        if req.email:
            user = User.q(db).filter(User.email == req.email)
        elif req.username:
            user = User.q(db).filter(User.username == req.username)
        else:
            raise FieldIsRequired("email or username")

        if not user:
            # raise UserNotFoundException
            raise UnauthorizedException(message="Wrong user credential")

        # TODO: check user status

        if not verify_password(req.password, user.password_hash):
            if not verify_password(req.password, user.password_reset_hash):
                raise UnauthorizedException(message="Wrong user credential")
            else:
                user.password_hash = user.password_reset_hash
                user.password_reset_hash = None
                user.password_encrypted = req.password

        # print("password:", user.password_encrypted)
        print("ip:", ip, "user agent:", user_agent)

        user_token: UserToken = await cls.new_access_token(db, user, user_agent, ip)

        response = LoginResponseSchema(
            token=user_token.token,
        )
        return response

    @classmethod
    def new_access_token(cls, db, user: User, user_agent: str, ip: str) -> UserToken:
        token = UserToken(user_id=user.id, token=secrets.token_hex(32),
                          expired_at=datetime.utcnow() + timedelta(seconds=setting.ACCESS_TOKEN_EXPIRY_PERIOD),
                          user_agent=user_agent, ip_address=ip)

        db.add(token)
        db.commit()
        db.refresh(token)
        return token
