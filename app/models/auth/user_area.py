from sqlmodel import SQLModel, Field, Relationship


class AuthUserArea(SQLModel, table=True):
    __tablename__ = "auth_user_area"

    user_id: int = Field(foreign_key="auth_user.id", primary_key=True, ondelete="CASCADE")
    area_id: int = Field(foreign_key="ref_area.id", primary_key=True, ondelete="CASCADE")
