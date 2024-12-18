import json
import asyncio

from app.db.models import User
from app.db.schemas import BaseUserCreate


async def migrate_users():
    with open("app/db_migrator/db/all_users.db", "r") as f:
        users_data = json.loads(f.read())
    models_dict = {}
    users = list(users_data.keys())
    for user in users:
        models_dict[user] = 10
    with open("app/db_migrator/db/got_count.db", "r") as f:
        users_rounds = json.loads(f.read())
    rounds = list(users_rounds.items())
    # print(rounds[0])
    for i in rounds:
        models_dict[i[0]] = i[1] if i[1] > 10 else 10

    for user in models_dict.items():
        print(user[0], user[1])
        user_exists = await User.get_by_tg_id(tg_id=user[0])
        if user_exists is None:
            user_model = BaseUserCreate(tg_id=user[0])
            user_db = await User.create(user_model)
            user_db.rounds = user[1]
            await user_db.save()