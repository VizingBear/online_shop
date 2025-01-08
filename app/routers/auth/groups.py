from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import noload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies import get_session
from app.models.auth.permission import AuthPermission
from app.models.auth.group import AuthGroup, AuthGroupsPublic, AuthGroupPublic, AuthGroupCreate

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("", response_model=AuthGroupsPublic, response_model_exclude_none=True)
async def read_groups(limit: int = 20, offset: int = 0, session: AsyncSession = Depends(get_session)):
    statement_data = select(AuthGroup).limit(limit).offset(offset).options(noload("*"))
    data = await session.scalars(statement_data)

    statement_count = select(func.count(AuthGroup.id))
    count = await session.scalar(statement_count)

    return AuthGroupsPublic(data=data, count=count)


@router.get("/{group_id}", response_model=AuthGroupPublic, response_model_exclude_none=True)
async def read_group(group_id: int, session: AsyncSession = Depends(get_session)):
    db_group = await session.get(AuthGroup, group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")

    return db_group


@router.post("", response_model=AuthGroupPublic, response_model_exclude_none=True)
async def create_group(group_create: AuthGroupCreate, session: AsyncSession = Depends(get_session)):
    statement = select(AuthPermission).where(AuthPermission.id.in_(group_create.permissions))

    group = AuthGroup.model_validate(
        group_create,
        update={
            "permissions": (await session.scalars(statement)).all(),
        }
    )

    session.add(group)
    await session.commit()

    return group


@router.put("/{group_id}", response_model=AuthGroupPublic, response_model_exclude_none=True)
async def update_group(group_id: int, group_update: AuthGroupCreate, session: AsyncSession = Depends(get_session)):
    db_group = await session.get(AuthGroup, group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")

    db_group.sqlmodel_update(group_update.model_dump())

    statement = select(AuthPermission).where(AuthPermission.id.in_(group_update.permissions))
    db_group.permissions = (await session.scalars(statement)).all()

    session.add(db_group)
    await session.commit()

    return db_group


@router.delete("/{group_id}", response_model=AuthGroupPublic, response_model_exclude_none=True)
async def delete_group(group_id: int, session: AsyncSession = Depends(get_session)):
    db_group = await session.get(AuthGroup, group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    await session.delete(db_group)

    await session.commit()

    return db_group
