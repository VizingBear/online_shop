from sqlmodel import SQLModel, Field, Relationship

from .group_permission import AuthGroupPermission
from .user_permission import AuthUserPermission


class AuthPermission(SQLModel, table=True):
    __tablename__ = "auth_permission"

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(max_length=255, unique=True)

    users: list["AuthUser"] = Relationship(back_populates="permissions", link_model=AuthUserPermission)
    groups: list["AuthGroup"] = Relationship(back_populates="permissions", link_model=AuthGroupPermission)


class AuthPermissionCreate(SQLModel):
    name: str


class AuthPermissionPublic(SQLModel):
    id: int
    name: str


class AuthPermissionsPublic(SQLModel):
    data: list[AuthPermissionPublic]
    count: int
