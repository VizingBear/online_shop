from sqlmodel import SQLModel, Field, Relationship


class AuthGroupPermission(SQLModel, table=True):
    __tablename__ = "auth_group_permission"

    permission_id: int = Field(foreign_key="auth_permission.id", primary_key=True, ondelete="CASCADE")
    group_id: int = Field(foreign_key="auth_group.id", primary_key=True, ondelete="CASCADE")
