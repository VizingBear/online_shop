from sqlmodel import SQLModel, Field, Relationship

from .group import AuthGroupPublic
from .permission import AuthPermissionPublic
from .user_area import AuthUserArea
from .user_group import AuthUserGroup
from .user_permission import AuthUserPermission


class AuthUser(SQLModel, table=True):
    __tablename__ = "auth_user"

    id: int | None = Field(primary_key=True, default=None)
    email: str = Field(max_length=255, unique=True)
    password: str
    name: str = Field(max_length=255)
    surname: str = Field(max_length=255)
    patronymic: str = Field(max_length=255)
    active: bool | None = Field(default=True)
    is_superuser: bool | None = Field(default=False)
    municipality_id: int = Field(foreign_key="ref_municipality.id", nullable=False)

    groups: list["AuthGroup"] = Relationship(
        back_populates="users",
        link_model=AuthUserGroup,
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    permissions: list["AuthPermission"] = Relationship(
        back_populates="users",
        link_model=AuthUserPermission,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    area: list["RefArea"] = Relationship(
        back_populates="users",
        link_model=AuthUserArea,
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class AuthUserPublic(SQLModel):
    id: int
    email: str
    name: str
    surname: str
    patronymic: str
    permissions: list[AuthPermissionPublic]
    groups: list[AuthGroupPublic]


class AuthUsersPublic(SQLModel):
    data: list[AuthUserPublic]
    count: int


class AuthUserCreate(SQLModel):
    email: str
    password: str
    name: str
    surname: str
    patronymic: str
    permissions: list[int]
    groups: list[int]
    is_superuser: bool


class AuthUserUpdate(SQLModel):
    email: str
    name: str
    surname: str
    patronymic: str
    permissions: list[int]
    groups: list[int]
    active: bool
    is_superuser: bool
