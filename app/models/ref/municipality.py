from sqlmodel import SQLModel, Field


class RefMunicipality(SQLModel, table=True):
    __tablename__ = "ref_municipality"

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(max_length=255)
    slug: str = Field(max_length=255)