from pydantic import BaseModel, ConfigDict, Field
from .user import UserRead

class SphereBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)

class SphereCreate(SphereBase):
    reader_ids: list[int] = []
    editor_ids: list[int] = []

class SphereUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)
    reader_ids: list[int] | None = None
    editor_ids: list[int] | None = None

class SphereInDBBase(SphereBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

class SphereRead(SphereInDBBase):
    owner: UserRead