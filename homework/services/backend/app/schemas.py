import uuid
from typing import List, Optional
from datetime import date

from pydantic import BaseModel, UUID4, field_validator, EmailStr


class BaseProperties(BaseModel):
    @field_validator("uuid", pre=True, always=True, check_fields=False)
    def default_hashed_id(cls, v):
        return v or uuid.uuid4()


class BaseUser(BaseProperties):
    uuid: Optional[UUID4] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    registration_date: Optional[date] = None
    is_admin: Optional[bool] = None


class UserCreate(BaseProperties):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseUser):
    uuid: UUID4
    username: str
    email: EmailStr
    registration_date: date
    is_admin: bool