from typing import Optional

from tortoise import fields, models
from tortoise.exceptions import DoesNotExist
from pydantic import UUID4

from app.base.base_models import BaseModel
from app.db.schemas import BaseUserCreate, BaseContourCreate, BaseWatermarkCreate, BaseWatermarkPictureCreate


class User(BaseModel):
    tg_id = fields.BigIntField()
    username = fields.CharField(max_length=128, null=True)
    first_name = fields.CharField(max_length=128, null=True)
    rounds = fields.IntField(default=10)
    is_admin = fields.BooleanField(default=False)
    full_access = fields.BooleanField(default=False)
    unlimited_time = fields.DateField(null=True)

    @classmethod
    async def get_by_tg_id(cls, tg_id: int) -> Optional["User"]:
        try:
            query = cls.get_or_none(tg_id=tg_id)
            user = await query
            return user
        except DoesNotExist:
            return None
        
    @classmethod
    async def get_by_username(cls, username: int) -> Optional["User"]:
        try:
            query = cls.get_or_none(username=username)
            user = await query
            return user
        except DoesNotExist:
            return None

    @classmethod
    async def create(cls, user: BaseUserCreate) -> "User":
        user_dict = user.model_dump()
        model = cls(**user_dict)
        await model.save()
        return model
    
    class Meta:
        table = "users"


class Contour(BaseModel):
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="saved_contours", to_field="uuid", on_delete=fields.CASCADE
    )
    title = fields.CharField(max_length=128)
    text = fields.CharField(max_length=128)
    font_text = fields.CharField(max_length=64)
    font_size = fields.IntField()
    font_weight = fields.IntField()
    text_color = fields.CharField(max_length=20)
    border = fields.IntField()
    border_color = fields.CharField(max_length=20)
    opacity = fields.FloatField()
    angle = fields.IntField()

    @classmethod
    async def get_by_id(cls, id: UUID4) -> Optional["Contour"]:
        try:
            query = cls.get_or_none(uuid=id)
            contour = await query
            return contour
        except DoesNotExist:
            return None

    @classmethod
    async def create(cls, contour: BaseContourCreate, user: User) -> "Contour":
        contour_dict = contour.model_dump()
        model = cls(**contour_dict, user=user)
        await model.save()
        return model

    class Meta:
        table = "contours"


class Watermark(BaseModel):
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="saved_watermarks", to_field="uuid", on_delete=fields.CASCADE
    )
    title = fields.CharField(max_length=128)
    opacity = fields.FloatField()
    offsetY = fields.IntField()
    offsetX = fields.IntField()

    @classmethod
    async def get_by_id(cls, id: UUID4) -> Optional["Watermark"]:
        try:
            query = cls.get_or_none(uuid=id)
            watermark = await query
            return watermark
        except DoesNotExist:
            return None
        
    @classmethod
    async def create(cls, watermark_in: BaseWatermarkCreate, user: User) -> "Watermark":
        watermark_db = watermark_in.model_dump()
        model = cls(**watermark_db, user=user)
        await model.save()
        return model
    
    class Meta:
        table = "watermarks"


class WatermarkPicture(models.Model):
    id = fields.IntField(pk=True, unique=True)
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="saved_watermark_pictures", to_field="uuid", on_delete=fields.CASCADE
    )
    file_path = fields.CharField(max_length=256)
    title = fields.CharField(max_length=64, null=True)

    @classmethod
    async def get_by_id(cls, id: int) -> Optional["WatermarkPicture"]:
        try:
            query = cls.get_or_none(id=id)
            picture = await query
            return picture
        except DoesNotExist:
            return None
        
    @classmethod
    async def create(cls, picture_in: BaseWatermarkPictureCreate, user: User) -> "WatermarkPicture":
        picture_db = picture_in.model_dump()
        model = cls(**picture_db, user=user)
        await model.save()
        return model
    
    class Meta:
        table = "watermark_pictures"