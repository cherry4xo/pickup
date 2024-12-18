import asyncio
import os
import time

from telebot.async_telebot import AsyncTeleBot

from app.redis.database import r
from app.settings.config import settings
from app.bot.handler import bot
from app.editing.utils import make_rounded, make_watermark
from app.db.models import Contour, Watermark
from app.bot.handler import States

async def send_rounded():
    try:
        while True:
            async with r.pipeline(transaction=True) as pipe:
                round_requests: dict = await (pipe.hgetall(
                    name="request"
                ).execute())

            if round_requests == [{}]:
                continue
            request = round_requests[0]
            if request["state"] == "default":
                await bot.send_video_note(chat_id=request["user_id"],
                                            data=open(request["file_path"], "rb"))

                async with r.pipeline(transaction=True) as pipe:
                    await (pipe.delete("request").execute())

                if os.path.exists(request["file_path"]):
                    os.remove(request["file_path"])
            elif request["state"] == "border":
                async with r.pipeline(transaction=True) as pipe:
                    border_request = (await (pipe.hgetall(
                        name=f"round_sample:{request['user_id']}",
                    ).execute()))[0]
                if border_request == {}:
                    continue
                async with r.pipeline(transaction=True) as pipe:
                    await (pipe.delete(f"round_sample:{request['user_id']}").execute())
                async with r.pipeline(transaction=True) as pipe:
                    await (pipe.delete("request").execute())
                sample_id = border_request[f"value"]
                sample = await Contour.get_by_id(id=sample_id)
                make_rounded(filename=request['file_path'], 
                             size=576, 
                             text=sample.text,
                             font_text=sample.font_text,
                             font_size=sample.font_size,
                             font_weight=sample.font_weight,
                             text_color=sample.text_color,
                             border=sample.border,
                             border_color=sample.border_color,
                             border_opacity=sample.border_opacity,
                             angle=sample.angle)
                filename_out = "".join(request["file_path"].split("."))[:-1] + "temp.mp4"
                await bot.send_video_note(chat_id=request["user_id"],
                                          data=open(filename_out, "rb"))

                if os.path.exists(request['file_path']):
                    os.remove(request['file_path'])
                if os.path.exists(filename_out):
                    os.remove(filename_out)
                await bot.set_state(user_id=request["user_id"], chat_id=request["user_id"], state=States.default_round)
            elif request["state"] == "watermark":
                async with r.pipeline(transaction=True) as pipe:
                    watermark_request = (await (pipe.hgetall(
                        name=f"watermark_sample:{request['user_id']}",
                    ).execute()))[0]
                if watermark_request == {}:
                    continue
                async with r.pipeline(transaction=True) as pipe:
                    await (pipe.delete(f"watermark_sample:{request['user_id']}").execute())
                async with r.pipeline(transaction=True) as pipe:
                    await (pipe.delete("request").execute())
                sample_id = border_request[f"value"]
                sample = await Watermark.get_by_id(id=sample_id)
                make_watermark(filename=request['file_path'],
                               opacity=sample.opacity,
                               picture_file_path=sample.picture_file_path)
                filename_out = "".join(request["file_path"].split("."))[:-1] + "temp.mp4"
                await bot.send_video_note(chat_id=request["user_id"],
                                          data=open(filename_out, "rb"))
                if os.path.exists(request['file_path']):
                    os.remove(request['file_path'])
                if os.path.exists(filename_out):
                    os.remove(filename_out)
                await bot.set_state(user_id=request["user_id"], chat_id=request["user_id"], state=States.default_round)
    except Exception as e:
            delay = 3
            text = f'Error: {e}, restarting after {delay} seconds'
            print(text)
            time.sleep(delay)
            text = f'Restarted'
            print(text)