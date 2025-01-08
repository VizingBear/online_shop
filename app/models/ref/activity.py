from datetime import date

from sqlmodel import SQLModel, Field


class RefActivity(SQLModel, table=True):
    __tablename__ = "ref_activity"

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(max_length=255)
    slug: str = Field(max_length=255)
    area_id: int = Field(foreign_key="ref_area.id", nullable=False)
    start_date: date = Field(nullable=False)
    end_date: date = Field(nullable=True)


    # users: list["AuthUser"] = Relationship(back_populates="groups", link_model=AuthUserGroup)
    # permissions: list["AuthPermission"] = Relationship(
    #     back_populates="groups",
    #     link_model=AuthGroupPermission,
    #     sa_relationship_kwargs={"lazy": "selectin"}
    # )