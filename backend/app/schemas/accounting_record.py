import math
from datetime import datetime
from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.accounting_record import OperationType
from .location import LocationRead
from .sphere import SphereRead
from .utils import PaginatedResponse


# Base properties
class RecordBase(BaseModel):
    description: str | None = Field(None, max_length=255)
    date: datetime | None = None


# Properties to receive on creation
class RecordCreateIncome(BaseModel):
    type: Literal["Income"]
    sum: float = Field(..., gt=0, description="Сумма должна быть положительной")
    location_id: int
    sphere_id: int


class RecordCreateSpend(BaseModel):
    type: Literal["Spend"]
    sum: float = Field(..., gt=0, description="Сумма должна быть положительной")
    location_id: int
    sphere_id: int


class RecordCreateTransfer(BaseModel):
    type: Literal["Transfer"]
    sum: float = Field(..., gt=0, description="Сумма должна быть положительной")
    description: str | None = Field(None, max_length=255)
    date: datetime | None = None
    
    # Nested discriminator for transfer type
    transfer_type: Literal["location", "sphere"]
    
    from_location_id: int | None = None
    to_location_id: int | None = None
    sphere_id: int | None = None # Required for location transfers

    from_sphere_id: int | None = None
    to_sphere_id: int | None = None
    location_id: int | None = None # Required for sphere transfers

    @model_validator(mode='after')
    def check_transfer_fields(self) -> 'RecordCreateTransfer':
        if self.transfer_type == 'location':
            if not all([self.from_location_id, self.to_location_id, self.sphere_id]):
                raise ValueError("For location transfer, 'from_location_id', 'to_location_id', and 'sphere_id' are required.")
            if self.from_location_id == self.to_location_id:
                raise ValueError("Source and destination locations cannot be the same.")
        elif self.transfer_type == 'sphere':
            if not all([self.from_sphere_id, self.to_sphere_id, self.location_id]):
                raise ValueError("For sphere transfer, 'from_sphere_id', 'to_sphere_id', and 'location_id' are required.")
            if self.from_sphere_id == self.to_sphere_id:
                 raise ValueError("Source and destination spheres cannot be the same.")
        return self


RecordCreate = Union[RecordCreateIncome, RecordCreateSpend, RecordCreateTransfer]
# Pydantic v2 needs Annotated for discriminated unions in some contexts, but FastAPI handles this well.
# For direct Pydantic usage, you might use:
# from typing import Annotated
# RecordCreate = Annotated[Union[...], Field(discriminator='type')]


# Properties to return to client
class RecordRead(RecordBase):
    id: int
    accounting_id: int
    operation_type: OperationType
    is_transfer: bool
    sum: float
    owner_id: int
    location: LocationRead | None
    sphere: SphereRead | None
    
    model_config = ConfigDict(from_attributes=True)


class PaginatedRecordRead(PaginatedResponse[RecordRead]):
    pass