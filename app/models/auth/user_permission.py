from sqlmodel import SQLModel, Field, Relationship


class AuthUserPermission(SQLModel, table=True):
    __tablename__ = "auth_user_permission"

    user_id: int = Field(foreign_key="auth_user.id", primary_key=True, ondelete="CASCADE")
    permission_id: int = Field(foreign_key="auth_permission.id", primary_key=True, ondelete="CASCADE")
