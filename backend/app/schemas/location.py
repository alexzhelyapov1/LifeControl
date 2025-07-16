from pydantic import BaseModel, ConfigDict, Field
from .user import UserRead

class LocationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)

class LocationCreate(LocationBase):
    reader_ids: list[int] = []
    editor_ids: list[int] = []

class LocationUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=255)
    reader_ids: list[int] | None = None
    editor_ids: list[int] | None = None

class LocationInDBBase(LocationBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

class LocationRead(LocationInDBBase):
    owner: UserRead