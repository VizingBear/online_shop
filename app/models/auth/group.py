from sqlmodel import SQLModel, Field, Relationship

from .permission import AuthPermission
from .group_permission import AuthGroupPermission
from .user_group import AuthUserGroup


class AuthGroup(SQLModel, table=True):
    __tablename__ = "auth_group"

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(max_length=255)

    users: list["AuthUser"] = Relationship(back_populates="groups", link_model=AuthUserGroup)
    permissions: list["AuthPermission"] = Relationship(
        back_populates="groups",
        link_model=AuthGroupPermission,
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class AuthGroupCreate(SQLModel):
    name: str
    permissions: list[int]


class AuthGroupPublic(SQLModel):
    id: int
    name: str
    permissions: list[AuthPermission]


class AuthGroupsPublic(SQLModel):
    data: list[AuthGroupPublic]
    count: int
