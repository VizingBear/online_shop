from sqlmodel import SQLModel, Field, Relationship


class AuthUserGroup(SQLModel, table=True):
    __tablename__ = "auth_user_group"

    user_id: int = Field(foreign_key="auth_user.id", primary_key=True, ondelete="CASCADE")
    group_id: int = Field(foreign_key="auth_group.id", primary_key=True, ondelete="CASCADE")
