from pydantic import BaseModel, ConfigDict, Field, EmailStr

# Base properties shared by all user-related schemas
class UserBase(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(None, max_length=255)

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = Field(None, min_length=8)

# Properties stored in DB
class UserInDBBase(UserBase):
    id: int
    is_admin: bool = False
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserInDBBase):
    hashed_password: str

# Properties to return to client
class UserRead(UserInDBBase):
    pass # For now, it's the same as UserInDBBase. Later we can add friends, etc.