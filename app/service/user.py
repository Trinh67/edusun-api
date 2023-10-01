import secrets
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.dto.core.user import LoginRequestSchema, LoginResponseSchema, CreateUserRequestSchema, \
    CreateUserResponseSchema, GetUserDetailResponseSchema, GetListUsersResponse, UpdateUserRequestSchema, \
    UpdateUserResponseSchema
from app.helper.custom_exception import FieldIsRequired, UnauthorizedException, ExistedException, ObjectNotFound
from app.helper.enum import UserType, UserRole, UserStatus, ObjectNotFoundType
from app.helper.pagination import Pagination
from app.model import User, UserToken
from app.helper.db import db_session
from app.utils.security_helpers import verify_password, get_password_hash
from setting import setting


class UserService:
    @classmethod
    def get_user_id_by_token(cls, token: str = None) -> Optional[int]:
        with next(db_session()) as db:
            user_token = UserToken.first(db, UserToken.token == token)

            if not user_token:
                # raise here return HTTP 500 error??
                # raise HTTPException(status_code=403, detail="Invalid Token")
                return None

            if user_token.expired_at < datetime.utcnow():
                # raise HTTPException(status_code=403, detail="Token expired")
                return None

            # TODO: check user status
            user = User.first(db, User.id == user_token.user_id)
            if not user or user.status != UserStatus.ACTIVE.value:
                # raise HTTPException(status_code=403, detail="User not found or blocked")
                return None

            return user_token.user_id

    @classmethod
    def is_admin(cls, user_id: int = None) -> bool:
        with next(db_session()) as db:
            user = User.first(db, User.id == user_id)
            if not user:
                return False

            if user.type != UserType.STAFF.value:
                return False

            if user.role not in [UserRole.ADMIN.value, UserRole.SUPER_ADMIN.value]:
                return False

            return True

    @classmethod
    def is_super_admin(cls, db: Session = db_session, user_id: int = None) -> bool:
        user = User.first(db, User.id == user_id)
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
            user = User.first(db, User.email == req.email, User.status == UserStatus.ACTIVE.value)
        elif req.phone:
            user = User.first(db, User.phone == req.phone, User.status == UserStatus.ACTIVE.value)
        else:
            raise FieldIsRequired("email or phone")

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

        user_token: UserToken = cls.new_access_token(db, user, user_agent, ip)

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

    @classmethod
    def create_user(
            cls, db: Session, req: CreateUserRequestSchema
    ) -> CreateUserResponseSchema:
        user = User.first(db, or_(User.email == req.email, User.phone == req.phone))
        if user:
            raise ExistedException(message="Email or phone already existed")

        new_user = User()
        for key, value in req.dict().items():
            setattr(new_user, key, value)
        # Find max id and generate code
        query = func.max(User.id)
        result = db.execute(query)
        max_id = result.scalars().first()
        new_user.code = f'US_{"{:06d}".format(max_id + 1)}' if max_id else 'US_000001'

        new_user.password_hash = get_password_hash(req.password)
        new_user.password = req.password
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return CreateUserResponseSchema(id=new_user.id)

    @classmethod
    def get_user_info(cls, db: Session, user_id: int) -> GetUserDetailResponseSchema:
        user = User.first(db, User.id == user_id)
        if not user:
            raise ObjectNotFound(obj=ObjectNotFoundType.USER.value)

        return GetUserDetailResponseSchema.from_orm(user)

    @classmethod
    def get_list_users(cls, db: Session, req_query, user_id: int):
        query = User.q(db)

        if req_query.user_type:
            query = query.filter(User.type == req_query.user_type.value)

        if req_query.user_status:
            query = query.filter(User.status == req_query.user_status.value)

        if req_query.search:
            query = query.filter(or_(User.email.ilike(f'%{req_query.search}%'),
                                     User.phone.ilike(f'%{req_query.search}%'),
                                     User.fullname.ilike(f'%{req_query.search}%')))

        total_items = query.count()
        query = query.order_by(User.created_at.desc())
        query = query.offset((req_query.page - 1) * req_query.page_size).limit(req_query.page_size)
        users = query.all()

        return GetListUsersResponse(users=[GetUserDetailResponseSchema.from_orm(u) for u in users]), \
               Pagination(current_page=req_query.page, page_size=req_query.page_size, total_items=total_items)

    @classmethod
    def update_user(cls, db: Session, user_id: int, req: UpdateUserRequestSchema):
        user = User.first(db, User.id == user_id)
        if not user:
            raise ObjectNotFound(obj=ObjectNotFoundType.USER.value)

        for key, value in req.dict().items():
            setattr(user, key, value)

        if req.password:
            user.password_hash = get_password_hash(req.password)
            user.password = req.password
        db.flush()
        db.commit()
        return UpdateUserResponseSchema(id=user.id)
