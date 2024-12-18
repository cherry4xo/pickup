import os
import var_dump
import json
import telebot
import uuid
from datetime import date

from yookassa import Payment
from PIL import ImageColor
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import StatesGroup, State
from telebot.types import LabeledPrice

from app.db.models import User, Contour, Watermark, WatermarkPicture
from app.db.schemas import BaseUserCreate, BaseContourCreate, BaseWatermarkCreate, BaseWatermarkPictureCreate
from app.bot import texts
from app.bot import menu
from app.redis.database import r
from app.settings.config import settings


state_storage = StateMemoryStorage()

bot = AsyncTeleBot(settings.TELEGRAM_BOT_TOKEN, state_storage=state_storage)

class States(StatesGroup):
    default_round = State()
    border_round = State()
    watermark_round = State()
    select_watermark_image = State()
    add_watermark_image = State()

# welcome_video = open("app/bot/answer_data/video1.mp4", "rb")
# marking_video_1 = open("app/bot/answer_data/marking_sample1.mp4", "rb")
# marking_video_2 = open("app/bot/answer_data/marking_sample2.mp4", "rb")


@bot.message_handler(commands=["make_sending"])
async def make_sending(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    if not user.is_admin:
        return await bot.send_message(message.chat.id, text=texts.is_not_admin_alert)
    
    users = await User.all()
    for user in users:
        try:
            await bot.send_photo(chat_id=user.tg_id,
                                 photo=open("app/bot/answer_data/arunov.jpg", "rb"),
                                 caption=texts.sending_text,
                                 reply_markup=menu.call_start_menu(),
                                 parse_mode="markdown")
        except:
            continue


@bot.callback_query_handler(func=lambda call: call.data.startswith("/start"))
async def welcome(call: telebot.types.CallbackQuery):
    await bot.set_state(call.message.from_user.id, States.default_round, call.message.chat.id)

    return await bot.send_video_note(chat_id=call.message.chat.id, 
                                     data=open("app/bot/answer_data/video1.mp4", "rb"), 
                                     reply_markup=menu.main_menu())


@bot.message_handler(commands=["start"])
async def welcome(message: telebot.types.Message):
    uid = int(message.from_user.id)

    user = await User.get_by_tg_id(tg_id=uid)

    if not user:
        username = message.from_user.username
        first_name = message.from_user.first_name
        user = await User.create(BaseUserCreate(tg_id=uid, first_name=first_name, username=username))

    if user.username != message.from_user.username:
        user.username = message.from_user.username
    if user.first_name != message.from_user.first_name:
        user.first_name = message.from_user.first_name

    await bot.set_state(message.from_user.id, States.default_round, message.chat.id)

    return await bot.send_video_note(chat_id=message.chat.id, 
                                     data=open("app/bot/answer_data/video1.mp4", "rb"), 
                                     reply_markup=menu.main_menu())
    

@bot.message_handler(content_types=["video"])
async def upload_video(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    if not user:
        username = message.from_user.username
        first_name = message.from_user.first_name
        user = await User.create(BaseUserCreate(tg_id=uid, first_name=first_name, username=username))

    if user.full_access:
        await bot.send_message(chat_id=message.chat.id, text=texts.unlimited_rounds)
    elif user.unlimited_time is not None:
        if user.unlimited_time > date.today():
            await bot.send_message(chat_id=message.chat.id, text=texts.unlimited_rounds)
    elif user.rounds > 0:
        user.rounds -= 1
        await user.save()
        await bot.send_message(chat_id=message.chat.id, text=texts.rounds_left(user.rounds))
    else:
        return await bot.send_message(chat_id=message.chat.id, text=texts.null_rounds)

    file_id = message.video.file_id
    file_info = await bot.get_file(message.video.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    new_file_path = f"app/data/{file_id}.mp4"
    with open(new_file_path, "wb") as file:
        file.write(downloaded_file)

    request_id = str(uuid.uuid4()) 

    if await bot.current_states.get_state(message.chat.id, message.from_user.id) == "States:default_round":
        state_r = "default"
    elif await bot.current_states.get_state(message.chat.id, message.from_user.id) == "States:border_round":
        state_r = "border"
    elif await bot.current_states.get_state(message.chat.id, message.from_user.id) == "States:watermark_round":
        state_r = "watermark"
    else:
        state_r = "default"

    data = {
        "id": request_id,
        "type": state_r,
        "user_id": user.tg_id,
        "file_path": f"{new_file_path}"
    }

    data_json = json.dumps(data)
    await r.lpush("request", data_json)


@bot.message_handler(content_types=["web_app_data"])
async def answer(webAppMes: telebot.types.Message):
    data = json.loads(webAppMes.web_app_data.data)
    if data["type"] == "contour":
        user = await User.get_by_tg_id(tg_id=webAppMes.from_user.id)
        data["border_color"] = data["border_color"][1:]
        border_color_rgb = tuple(int(data["border_color"][i:i+2], 16) for i in (0, 2, 4))
        data["border_color"] = f"rgb({border_color_rgb[0]}, {border_color_rgb[1]}, {border_color_rgb[2]})"
        data["text_color"] = data["text_color"][1:]
        text_color_rgb = tuple(int(data["text_color"][i:i+2], 16) for i in (0, 2, 4))
        data["text_color"] = f"rgb({text_color_rgb[0]}, {text_color_rgb[1]}, {text_color_rgb[2]})"
        data["angle"] = int(data["angle"]) + 90
        contour_db = BaseContourCreate(**data)
        contour = await Contour.create(contour=contour_db, user=user)
        await bot.send_message(chat_id=webAppMes.chat.id, text=texts.contour_saved(title=contour_db.title))
    if data["type"] == "text":
        user = await User.get_by_tg_id(tg_id=webAppMes.from_user.id)
        watermark_db = BaseWatermarkCreate(**data)
        watermark = await Watermark.create(watermark_in=watermark_db, user=user)
        await bot.send_message(chat_id=webAppMes.chat.id, text=texts.contour_saved(title=watermark_db.title))


@bot.message_handler(func=lambda x: x.text == texts.branding)
async def saved_samples(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.send_video_note(chat_id=message.chat.id, 
                              data=open("app/bot/answer_data/arunov_branding.mp4", "rb"))

    await bot.send_message(chat_id=message.chat.id, 
                           text=texts.watermark_menu_text, 
                           reply_markup=menu.branding_menu())
    

@bot.message_handler(func=lambda x: x.text == texts.video_marking)
async def get_marking_menu(message: telebot.types.Message):
    await bot.send_video_note(chat_id=message.chat.id, 
                              data=open("app/bot/answer_data/arunov_marking1.mp4", "rb"))

    await bot.send_video_note(chat_id=message.chat.id, 
                              data=open("app/bot/answer_data/arunov_marking2.mp4", "rb"))

    await bot.send_message(chat_id=message.chat.id,
                           text=texts.round_menu_text,
                           reply_markup=menu.marking_menu())
                        #    reply_markup=await menu.round_samples_menu(to_user=user))
    

@bot.message_handler(func=lambda x: x.text == texts.back_to_main_menu)
async def get_main_menu(message: telebot.types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=texts.main_menu,
                           reply_markup=menu.main_menu())


@bot.message_handler(func=lambda x: x.text == texts.create_marked_video)
async def get_saved_samples(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.send_message(text=texts.text_round_samples, 
                           chat_id=message.chat.id,
                           reply_markup=await menu.round_samples_menu(user))
    

@bot.message_handler(func=lambda x: x.text == texts.delete_sample_marking)
async def delete_marking_sample(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.send_message(text=texts.delete_sample_menu_text,
                           chat_id=message.chat.id,
                           reply_markup=await menu.delete_marking_sample_menu(to_user=user))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_marking_menu"))
async def delete_marking_sample(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.edit_message_text(text=texts.delete_sample_menu_text,
                                message_id=call.message.id,
                                chat_id=call.message.chat.id,
                                reply_markup=await menu.delete_marking_sample_menu(to_user=user))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_m_"))
async def delete_marking_sample_confirm(call: telebot.types.CallbackQuery):
    sample_id = call.data.split("_")[-1]
    sample = await Contour.get_by_id(id=sample_id)

    await bot.edit_message_text(text=texts.delete_sample_confirm(sample_name=sample.title),
                                message_id=call.message.id,
                                chat_id=call.message.chat.id,
                                reply_markup=await menu.delete_marking_sample_confirm_menu(id=sample_id))


@bot.callback_query_handler(func=lambda call: call.data.startswith("conf_del_m_"))
async def deleted_marking_sample(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    sample_id = call.data.split("_")[-1]
    sample = await Contour.get_by_id(id=sample_id)
    await sample.delete()

    await bot.edit_message_text(text=texts.deleted_sample(sample_name=sample.title),
                                message_id=call.message.id,
                                chat_id=call.message.chat.id)
    await bot.send_message(text=texts.delete_sample_menu_text,
                           chat_id=call.message.chat.id,
                           reply_markup=await menu.delete_marking_sample_menu(to_user=user))

    
@bot.message_handler(func=lambda x: x.text == texts.delete_sample_branding)
async def delete_marking_branding(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.send_message(text=texts.delete_sample_menu_text,
                           chat_id=message.chat.id,
                           reply_markup=await menu.delete_branding_sample_menu(to_user=user))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_branding_menu"))
async def delete_marking_branding(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.edit_message_text(text=texts.delete_sample_menu_text,
                                message_id=call.message.id,
                                chat_id=call.message.chat.id,
                                reply_markup=await menu.delete_branding_sample_menu(to_user=user))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_b_"))
async def delete_marking_sample_confirm(call: telebot.types.CallbackQuery):
    sample_id = call.data.split("_")[-1]
    sample = await Watermark.get_by_id(id=sample_id)

    await bot.edit_message_text(text=texts.delete_sample_confirm(sample_name=sample.title),
                                message_id=call.message.id,
                                chat_id=call.message.chat.id,
                                reply_markup=await menu.delete_branding_sample_confirm_menu(id=sample_id))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("conf_del_b_"))
async def deleted_marking_sample(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    sample_id = call.data.split("_")[-1]
    sample = await Watermark.get_by_id(id=sample_id)
    await sample.delete()

    await bot.edit_message_text(text=texts.deleted_sample(sample_name=sample.title),
                                message_id=call.message.id,
                                chat_id=call.message.chat.id)
    await bot.send_message(text=texts.delete_sample_menu_text,
                           chat_id=call.message.chat.id,
                           reply_markup=await menu.delete_branding_sample_menu(to_user=user))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("pictures_menu"))
async def pictures_menu(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.edit_message_text(text=texts.watermark_pictures_menu_text,
                                chat_id=call.message.chat.id,
                                message_id=call.message.id,
                                reply_markup=await menu.watermark_pictures_menu(user))


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_picture"))
async def delete_picture(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.edit_message_text(text=texts.delete_picture_menu_text,
                                message_id=call.message.id,
                                chat_id=call.message.chat.id,
                                reply_markup=await menu.delete_pictures_menu(to_user=user))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_p_"))
async def delete_picture_confirm(call: telebot.types.CallbackQuery):
    picture_id = call.data.split("_")[-1]
    picture = await WatermarkPicture.get_by_id(id=picture_id)

    await bot.edit_message_text(text=texts.delete_picture_confirm(picture_name=picture.title),
                                message_id=call.message.id,
                                chat_id=call.message.chat.id,
                                reply_markup=await menu.delete_pictures_confirm_menu(picture_id=picture.id))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("conf_del_p_"))
async def deleted_picture(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    picture_id = call.data.split("_")[-1]
    picture = await WatermarkPicture.get_by_id(id=picture_id)
    await picture.delete()
    if os.path.exists(picture.file_path):
        os.remove(picture.file_path)

    await bot.edit_message_text(text=texts.deleted_picture(picutre_name=picture.title),
                                message_id=call.message.id,
                                chat_id=call.message.chat.id)
    await bot.send_message(text=texts.delete_picture_menu_text,
                           chat_id=call.message.chat.id,
                           reply_markup=await menu.delete_pictures_menu(to_user=user))


@bot.message_handler(func=lambda x: x.text == texts.create_branded_video)
async def get_saved_branding_samples(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.send_message(text=texts.text_pick_picture,
                           chat_id=message.chat.id,
                           reply_markup=await menu.watermark_pictures_menu(user))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("back_watermark_pictures"))
async def get_saved_watermark_samples(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.edit_message_text(text=texts.watermark_pictures_menu_text,
                                chat_id=call.message.chat.id,
                                message_id=call.message.id,
                                reply_markup=await menu.watermark_pictures_menu(user))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("watermark_new_picture"))
async def add_new_watermark_picture(call: telebot.types.CallbackQuery):
    uid = call.from_user.id

    await bot.set_state(user_id=uid, state=States.add_watermark_image, chat_id=call.message.chat.id)
    await bot.edit_message_text(text=texts.watermark_add_new_picture,
                                chat_id=call.message.chat.id,
                                message_id=call.message.id)
    

@bot.message_handler(content_types=["document"], state=States.add_watermark_image)
async def new_watermark_picute_handler(message: telebot.types.Message):
    if message.caption is None:
        return await bot.send_message(chat_id=message.chat.id,
                                      text=texts.none_capture_error)

    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    if message.document.file_name.split('.')[-1].lower() != "png":
        return await bot.send_message(chat_id=message.chat.id, 
                                      text=texts.invalid_extention_error, 
                                      reply_markup=await menu.watermark_pictures_menu(to_user=user))
    downloaded_file = await bot.download_file(file_info.file_path)
    new_file_path = f"app/data/{file_id}.png"
    with open(new_file_path, "wb") as file:
        file.write(downloaded_file)

    watermark_picture_db = BaseWatermarkPictureCreate(file_path=new_file_path, title=message.caption)
    await WatermarkPicture.create(picture_in=watermark_picture_db, user=user)
    await bot.send_message(chat_id=message.chat.id, 
                           text=texts.watermark_added_picture, 
                           reply_markup=await menu.watermark_pictures_menu(to_user=user))
    await bot.set_state(user_id=uid, state=States.default_round, chat_id=message.chat.id)


@bot.message_handler(content_types=["photo"], state=States.add_watermark_image)
async def photo_recieve_notification(message: telebot.types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=texts.invalid_extention_error)
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("watermark_picture_"))
async def choose_watermark_sample(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    picture_id = "".join(call.data.split("_")[2:])

    await bot.edit_message_text(text=texts.text_watermark_samples,
                                chat_id=call.message.chat.id,
                                message_id=call.message.id,
                                reply_markup=await menu.watermark_samples_menu(to_user=user, picture_id=picture_id))
    

# @bot.callback_query_handler(func=lambda call: call.data.startswith("back_watermark_pictures"))
# async def back_watermark_pictures(call: telebot.types.CallbackQuery):
#     uid = call.message.from_user.id
#     user = await User.get_by_tg_id(tg_id=uid)

#     await bot.edit_message_text(chat_id=call.message.chat.id, 
#                                 text=texts.watermark_menu_text, 
#                                 message_id=call.message.id,
#                                 reply_markup=await menu.watermark_pictures_menu(to_user=user))


# @bot.callback_query_handler(func=lambda call: call.data.startswith("back_watermark_samples"))
# async def saved_watermark_samples(call: telebot.types.CallbackQuery):
#     uid = call.message.from_user.id
#     user = await User.get_by_tg_id(tg_id=uid)
#     await bot.edit_message_text(chat_id=call.message.chat.id, 
#                                 text=texts.watermark_menu_text, 
#                                 message_id=call.message.id,
#                                 reply_markup=await menu.watermark_samples_menu(to_user=user))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("back_round_samples"))
async def saved_round_samples(call: telebot.types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                text=texts.round_menu_text,
                                message_id=call.message.id,
                                reply_markup=menu.round_samples_menu())


@bot.callback_query_handler(func=lambda call: call.data.startswith("round_sample_"))
async def set_state_round_sample_video(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.set_state(user.tg_id, States.border_round, call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, text=texts.on_set_border_round_state, message_id=call.message.id)

    async with r.pipeline(transaction=True) as pipe:
        await (pipe.hset(
            name=f"{user.tg_id}:round_sample",
            mapping={
                "sample_id": "".join(call.data.split('_')[2:]),
            }
        ).execute())

    return


@bot.callback_query_handler(func=lambda call: call.data.startswith("w_s_"))
async def set_state_watermark_sample_video(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    await bot.set_state(user.tg_id, States.watermark_round, call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, text=texts.on_set_watermark_round_state, message_id=call.message.id)

    print(await bot.current_states.get_state(call.message.chat.id, call.from_user.id))

    async with r.pipeline(transaction=True) as pipe:
        await (pipe.hset(
            name=f"{user.tg_id}:watermark_sample",
            mapping={
                "sample_id": "".join(call.data.split('_')[2:3]),
                "picture_id": "".join(call.data.split('_')[3:4])
            }
        ).execute())
    return


@bot.message_handler(commands=["set_unlimited_sub"])
async def set_full_access(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    if not user.is_admin:
        return await bot.send_message(message.chat.id, text=texts.is_not_admin_alert)

    to_user_id = message.text.split(" ")[-1]
    to_user = await User.get_by_tg_id(tg_id=to_user_id)

    if not to_user:
        return await bot.send_message(message.chat.id, text=texts.user_not_exist_alert(id=to_user_id))
    
    to_user.full_access = True
    await to_user.save()
    return await bot.send_message(message.chat.id, text=texts.user_unlimited(id=to_user_id))


@bot.message_handler(commands=["cancel_unlimited_sub"])
async def cancel_full_access(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    if not user.is_admin:
        return await bot.send_message(message.chat.id, text=texts.is_not_admin_alert)

    to_user_id = message.text.split(" ")[-1]
    to_user = await User.get_by_tg_id(tg_id=to_user_id)

    if not to_user:
        return await bot.send_message(message.chat.id, text=texts.user_not_exist_alert(id=to_user_id))
    
    to_user.full_access = False
    await to_user.save()
    return await bot.send_message(message.chat.id, text=texts.user_limited(id=to_user_id))


@bot.message_handler(commands=["set_year_sub"])
async def set_year_sub(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    if not user.is_admin:
        return await bot.send_message(message.chat.id, text=texts.is_not_admin_alert)

    to_user_id = message.text.split(" ")[-1]
    to_user = await User.get_by_tg_id(tg_id=to_user_id)

    if not to_user:
        return await bot.send_message(message.chat.id, text=texts.user_not_exist_alert(id=to_user_id))
    
    to_user.unlimited_time = date(year=date.today().year + 1, month=date.today().month, day=date.today().day)
    await to_user.save()
    return await bot.send_message(message.chat.id, text=texts.user_set_sub(id=to_user_id))


@bot.message_handler(commands=["cancel_year_sub"])
async def cancel_year_sub(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    if not user.is_admin:
        return await bot.send_message(message.chat.id, text=texts.is_not_admin_alert)

    to_user_id = message.text.split(" ")[-1]
    to_user = await User.get_by_tg_id(tg_id=to_user_id)

    if not to_user:
        return await bot.send_message(message.chat.id, text=texts.user_not_exist_alert(id=to_user_id))
    
    to_user.unlimited_time = None
    await to_user.save()
    return await bot.send_message(message.chat.id, text=texts.user_cancel_sub(id=to_user_id))


@bot.message_handler(commands=["users"])
async def users_count(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    if not user.is_admin:
        return await bot.send_message(message.chat.id, text=texts.is_not_admin_alert)
    
    count = await User.all().count()
    return await bot.send_message(message.chat.id, text=texts.users_count(count))


@bot.message_handler(func=lambda x: x.text == texts.upload_video)
async def upload_video_message(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, States.default_round, message.chat.id)
    return await bot.send_message(message.chat.id, text=texts.upload_video_answer)


# @bot.message_handler(func=lambda x: x.text == texts.instruction)
# async def instruction(message: telebot.types.Message):
#     return await bot.send_message(message.chat.id, text=texts.instruction_answer, disable_web_page_preview=True)


@bot.message_handler(func=lambda x: x.text == texts.payment)
async def payment_message(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(uid)

    if user.full_access:
        rounds = -1
    elif user.unlimited_time is not None:
        if user.unlimited_time > date.today():
            rounds = -2
    else:
        rounds = user.rounds
    return await bot.send_message(message.chat.id, text=texts.payment_answer(rounds), reply_markup=menu.tariff())
    

@bot.callback_query_handler(func=lambda call: call.data.startswith("tariff"))
async def tariff(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    count, total = call.data.split("_")[1:3]

    # prices = [LabeledPrice(label=texts.value(count), amount=f"{total}00")]
    
    # await bot.send_invoice(call.message.chat.id,
    #                        title=texts.price(count, total),
    #                        description=texts.buy_rounds(count, total),
    #                        invoice_payload=f"{count}",
    #                        provider_token=settings.PROVIDER_TOKEN,
    #                        currency="rub",
    #                        prices=prices)
    
    async with r.pipeline(transaction=True) as pipe:
        payment = (await (pipe.hgetall(
            f"{user.uuid}:payment_id"
        ).execute()))[0]

    if payment != {}:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=texts.payment_already_sent
        )
        return

    idempotence_key = str(uuid.uuid4())
    res = Payment.create(
        {
            "amount": {
                "value": total,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://yoomoney.ru/"
            },
            "capture": True,
            "metadata": {
                "count": f"{count}"
            },
            "description": f"{count} кружочков"
        },
        idempotence_key 
    )

    payment_url = res.confirmation.confirmation_url

    await bot.edit_message_text(
        text=texts.payment_url_and_test(url=payment_url, count=count, total=total),
        chat_id=call.message.chat.id,
        message_id=call.message.id
    )

    async with r.pipeline(transaction=True) as pipe:
        await (pipe.hset(
            f"{user.uuid}:payment_id",
            mapping={
                "id": res.id
            }
        ).execute())


@bot.callback_query_handler(func=lambda call: call.data.startswith("check_payment"))
async def check_payment(call: telebot.types.CallbackQuery):
    uid = call.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)

    async with r.pipeline(transaction=True) as pipe:
        payment = (await (pipe.hgetall(
            f"{user.uuid}:payment_id"
        ).execute()))[0]

        if payment == {}:
            return await bot.send_message(
                chat_id=call.message.chat.id,
                text=texts.payment_not_sent,
            )

        confirmed = Payment.find_one(payment_id=payment["id"])
        if confirmed.status == "succeeded":
            user.rounds += int(confirmed.metadata["count"])
            await user.save()

            await (pipe.delete(f"{user.uuid}:payment_id").execute())

            return await bot.send_message(
                chat_id=call.message.chat.id,
                text=texts.got_payment(count=confirmed.metadata["count"], total=user.rounds)
            )
        
        elif confirmed.status == "canceled":
            await (pipe.delete(f"{user.uuid}:payment_id").execute())

            return await bot.send_message(
                chat_id=call.message.chat.id,
                text=texts.cancelled_payment
            )
        
        elif confirmed.status == "pending":
            return await bot.send_message(
                chat_id=call.message.chat.id,
                text=texts.pending_payment
            )
        
        else:
            await (pipe.delete(f"{user.uuid}:payment_id").execute())
            
            await bot.send_message(
                chat_id=call.message.chat.id,
                text=texts.expired_payment
            )
            return


@bot.message_handler(func=lambda x: x.text == texts.contest)
async def give_bot(message: telebot.types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=texts.give_bot,
        parse_mode="markdown"
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
async def checkout(pre_checkout_query: telebot.types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message=texts.payment_error_message)
    

@bot.message_handler(content_types=["successful_payment"])
async def got_payment(message: telebot.types.Message):
    uid = message.from_user.id
    user = await User.get_by_tg_id(tg_id=uid)
    count = message.successful_payment.invoice_payload
    
    user.rounds += int(count)
    await user.save()
    total = user.rounds
    return await bot.send_message(message.chat.id,
                                  text=texts.got_payment(count, total))


@bot.message_handler(func=lambda x: x.text == texts.technical_support)
async def technical_support(message: telebot.types.Message):
    return await bot.send_message(message.chat.id, text=texts.technical_support_answer)
