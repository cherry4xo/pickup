import os

from asyncio import sleep
from tortoise import Tortoise
from yookassa import Configuration

from app.db.models import User
from app.redis.database import ping_redis_connection, r
from app.db_migrator.migrate import migrate_users

from app.settings.config import settings

def get_app_list():
    app_list = [f"{settings.APPLICATIONS_MODULE}.{app}.models" for app in settings.APPLICATIONS]
    return app_list

async def init(db_url: str | None = None):
    await Tortoise.init(
        db_url=db_url or settings.DB_URL,
        modules={"models": get_app_list()}
    )

    await Tortoise.generate_schemas()
    print(f"Connected to DB")
    await ping_redis_connection(r)

    if not os.path.exists("app/data"):
        os.mkdir("app/data")

    Configuration.configure(
        account_id=settings.SHOP_ID,
        secret_key=settings.YOO_SECRET
    )

    # await migrate_users()


async def create_default_admin_user():
    await sleep(3)
    user = await User.get_by_tg_id(tg_id=settings.DEFAULT_ADMIN_TG_ID)
    if user and user.is_admin:
        return

    if not user:
        user = User()

    user.username = settings.DEFAULT_ADMIN_USERNAME
    user.first_name = settings.DEFAULT_ADMIN_FIRST_NAME
    user.tg_id = settings.DEFAULT_ADMIN_TG_ID
    user.is_admin = True
    await user.save()
    return user

