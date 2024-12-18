import uuid
from typing import Optional
from pydantic import BaseModel, validator, UUID4


class BaseProperties(BaseModel):
    @validator("uuid", pre=True, always=True, check_fields=False)
    def default_hashed_id(cls, v):
        return v or uuid.uuid4()


class BaseUserCreate(BaseProperties):
    tg_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None

    class Config:
        from_attributes = True


class BaseContourCreate(BaseProperties):
    title: str
    text: str
    font_text: str
    font_size: int
    font_weight: int
    text_color: str
    border: int
    border_color: str
    opacity: float
    angle: float

    class Config:
        from_attributes = True


class BaseWatermarkCreate(BaseProperties):
    title: str
    opacity: float
    offsetY: int
    offsetX: int

    class Config:
        from_attributes = True


class BaseWatermarkPictureCreate(BaseProperties):
    title: Optional[str] = None
    file_path: str

    class Config:
        from_attributes = True