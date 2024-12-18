import json
import asyncio
import os
import time

from app.redis.database import r
from app.settings.config import settings
from app.bot.handler import bot, States
from app.editing.utils import make_watermark, make_rounded, make_default_rounded
from app.db.models import Contour, Watermark, WatermarkPicture

async def send_rounded() -> None:
    while True:
        try:
            await asyncio.sleep(0.25)
            request = await r.rpop("request")
            if request is None:
                continue
            data = json.loads(request)
            if data["type"] == "default":
                make_default_rounded(filename=data["file_path"])
                filename_out = "".join(data["file_path"].split("."))[:-1] + "temp.mp4"
                await bot.send_video_note(chat_id=data["user_id"],
                                          data=open(filename_out, "rb"))
                await bot.set_state(user_id=data["user_id"], chat_id=data["user_id"], state=States.default_round)
                if os.path.exists(data["file_path"]):
                    os.remove(data["file_path"])
                if os.path.exists(filename_out):
                    os.remove(filename_out)
            elif data["type"] == "border":
                async with r.pipeline(transaction=True) as pipe:
                    round_sample_data = (await pipe.hgetall(name=f"{data['user_id']}:round_sample").execute())[0]
                    await (pipe.delete(f"{data['user_id']}:round_sample").execute())
                round_sample_id = round_sample_data["sample_id"]
                sample = await Contour.get_by_id(id=round_sample_id)
                make_rounded(
                    filename=data["file_path"],
                    size=576,
                    text=sample.text,
                    font_text=sample.font_text,
                    font_size=sample.font_size,
                    font_weight=sample.font_weight,
                    text_color=sample.text_color,
                    border=sample.border,
                    border_color=sample.border_color,
                    border_opacity=sample.opacity,
                    angle=sample.angle
                )
                filename_out = "".join(data["file_path"].split("."))[:-1] + "temp.mp4"
                await bot.send_video_note(chat_id=data["user_id"],
                                          data=open(filename_out, "rb"))
                if os.path.exists(data['file_path']):
                    os.remove(data['file_path'])
                if os.path.exists(filename_out):
                    os.remove(filename_out)
                await bot.set_state(user_id=data["user_id"], chat_id=data["user_id"], state=States.default_round)

            elif data["type"] == "watermark":
                async with r.pipeline(transaction=True) as pipe:
                    watermark_sample_data = (await pipe.hgetall(name=f"{data['user_id']}:watermark_sample").execute())[0]
                    await (pipe.delete(f"{data['user_id']}:watermark_sample").execute())
                watermark_sample_id = watermark_sample_data["sample_id"]
                picture_id = watermark_sample_data["picture_id"]
                sample = await Watermark.get_by_id(id=watermark_sample_id)
                picture = await WatermarkPicture.get_by_id(id=picture_id)
                make_watermark(
                    filename=data["file_path"],
                    opacity=sample.opacity,
                    offsetX=sample.offsetX,
                    offsetY=sample.offsetY,
                    picture_file_path=picture.file_path
                )
                filename_out = "".join(data["file_path"].split("."))[:-1] + "temp.mp4"
                await bot.send_video_note(chat_id=data["user_id"],
                                          data=open(filename_out, "rb"))
                if os.path.exists(data['file_path']):
                    os.remove(data['file_path'])
                if os.path.exists(filename_out):
                    os.remove(filename_out)
                await bot.set_state(user_id=data["user_id"], chat_id=data["user_id"], state=States.default_round)
    
        except Exception as e:
            delay = 3
            text = f'Error: {e}, restarting after {delay} seconds'
            print(text)
            time.sleep(delay)
            text = f'Restarted'
            print(text)