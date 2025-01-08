from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies import get_session
from app.models.auth.permission import AuthPermissionsPublic, AuthPermission, AuthPermissionCreate, AuthPermissionPublic

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("", response_model=AuthPermissionsPublic, response_model_exclude_none=True)
async def read_permissions(limit: int = 20, offset: int = 0, session: AsyncSession = Depends(get_session)):
    statement_data = select(AuthPermission).limit(limit).offset(offset)
    data = await session.scalars(statement_data)

    statement_count = select(func.count(AuthPermission.id))
    count = await session.scalar(statement_count)

    return AuthPermissionsPublic(data=data, count=count)


@router.get("/{permission_id}", response_model=AuthPermissionPublic, response_model_exclude_none=True)
async def read_permission(permission_id: int, session: AsyncSession = Depends(get_session)):
    db_permission = await session.get(AuthPermission, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    return db_permission


@router.post("", response_model=AuthPermissionCreate, response_model_exclude_none=True)
async def create_permission(permission_create: AuthPermissionCreate, session: AsyncSession = Depends(get_session)):
    permission = AuthPermission.model_validate(permission_create)

    session.add(permission)
    await session.commit()

    return permission


@router.put("/{permission_id}", response_model=AuthPermissionPublic, response_model_exclude_none=True)
async def update_permission(
    permission_id: int,
    permission_update: AuthPermissionCreate,
    session: AsyncSession = Depends(get_session)
):
    db_permission = await session.get(AuthPermission, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db_permission.sqlmodel_update(permission_update.model_dump())

    session.add(db_permission)
    await session.commit()

    return db_permission


@router.delete("/{permission_id}",  response_model=AuthPermissionPublic, response_model_exclude_none=True)
async def delete_permission(permission_id: int, session: AsyncSession = Depends(get_session)):
    db_permission = await session.get(AuthPermission, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    await session.delete(db_permission)
    await session.commit()

    return db_permission
