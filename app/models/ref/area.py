from sqlmodel import SQLModel, Field, Relationship
from ..auth.user_area import AuthUserArea


class RefArea(SQLModel, table=True):
    __tablename__ = "ref_area"

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(max_length=255)
    slug: str = Field(max_length=255)

    users: list["AuthUser"] = Relationship(back_populates="area", link_model=AuthUserArea)
