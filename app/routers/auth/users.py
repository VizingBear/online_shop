from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy import func
from sqlalchemy.orm import noload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies import get_session
from app.models.auth.group import AuthGroup
from app.models.auth.permission import AuthPermission
from app.models.auth.user import AuthUsersPublic, AuthUser, AuthUserCreate, AuthUserPublic, AuthUserUpdate

router = APIRouter(prefix="/users", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("", response_model=AuthUsersPublic, response_model_exclude_none=True)
async def read_users(limit: int = 20, offset: int = 0, session: AsyncSession = Depends(get_session)):
    statement_data = select(AuthUser).limit(limit).offset(offset).options(noload("*"))
    data = await session.scalars(statement_data)

    statement_count = select(func.count(AuthUser.id))
    count = await session.scalar(statement_count)

    return AuthUsersPublic(data=data, count=count)


@router.get("/{user_id}", response_model=AuthUserPublic, response_model_exclude_none=True)
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(AuthUser).where(AuthUser.id == user_id)
    db_user = await session.scalar(statement)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return AuthUserPublic.model_validate(db_user)


@router.post("", response_model=AuthUserPublic, response_model_exclude_none=True)
async def create_user(user_create: AuthUserCreate, session: AsyncSession = Depends(get_session)):
    statement_group = select(AuthGroup).where(AuthGroup.id.in_(user_create.groups))
    statement_permission = select(AuthPermission).where(AuthPermission.id.in_(user_create.permissions))

    user = AuthUser.model_validate(
        user_create,
        update={
            "password": pwd_context.hash(user_create.password),
            "groups": (await session.scalars(statement_group)).all(),
            "permissions": (await session.scalars(statement_permission)).all(),
            "active": True
        }
    )

    session.add(user)
    await session.commit()

    return user


@router.put("/{user_id}", response_model=AuthUserPublic, response_model_exclude_none=True)
async def update_user(user_id: int, user_update: AuthUserUpdate, session: AsyncSession = Depends(get_session)):
    db_user = await session.get(AuthUser, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.sqlmodel_update(user_update.model_dump(exclude_none=True))

    statement = select(AuthGroup).where(AuthGroup.id.in_(user_update.groups))
    db_user.groups = (await session.scalars(statement)).all()

    statement = select(AuthPermission).where(AuthPermission.id.in_(user_update.permissions))
    db_user.permissions = (await session.scalars(statement)).all()

    session.add(db_user)
    await session.commit()

    return db_user


@router.delete("/{user_id}", response_model=AuthUserPublic, response_model_exclude_none=True)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    db_user = await session.get(AuthUser, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(db_user)

    await session.commit()

    return db_user
