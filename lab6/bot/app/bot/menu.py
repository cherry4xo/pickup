from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from pydantic import UUID4

from app.db.models import User, Contour, Watermark, WatermarkPicture
from app.bot import texts


def call_start_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Обновить", callback_data="/start"))
    return keyboard


def main_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    # marking_app = WebAppInfo("https://tgweb.cherry4xo.ru", )
    # branding_app = WebAppInfo("https://t.me/cherry4xo_round_bot/rounded")
    keyboard.add(KeyboardButton(text=texts.upload_video))
    keyboard.add(KeyboardButton(text=texts.branding))
    keyboard.add(KeyboardButton(text=texts.video_marking)) # , web_app=marking_app
    # keyboard.add(KeyboardButton(text=texts.video_labeling, web_app=marking_app))
    keyboard.add(KeyboardButton(text=texts.contest))
    keyboard.add(KeyboardButton(text=texts.payment))
    # keyboard.add(KeyboardButton(text=texts.check_payment))
    keyboard.add(KeyboardButton(text=texts.technical_support))

    return keyboard


def marking_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    marking_app = WebAppInfo("https://arunov-round.ru/?mode=contour")
    keyboard.add(KeyboardButton(text=texts.create_sample, web_app=marking_app))
    keyboard.add(KeyboardButton(text=texts.delete_sample_marking))
    keyboard.add(KeyboardButton(text=texts.create_marked_video))
    keyboard.add(KeyboardButton(text=texts.back_to_main_menu))

    return keyboard


def branding_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    branding_app = WebAppInfo("https://arunov-round.ru/?mode=text")
    keyboard.add(KeyboardButton(text=texts.create_sample, web_app=branding_app))
    keyboard.add(KeyboardButton(text=texts.delete_sample_branding))
    keyboard.add(KeyboardButton(text=texts.create_branded_video))
    keyboard.add(KeyboardButton(text=texts.back_to_main_menu))

    return keyboard


async def delete_marking_sample_menu(to_user: User) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    saved_samples = await Contour.filter(user=to_user)
    for sample in saved_samples:
        keyboard.add(InlineKeyboardButton(text=sample.title, callback_data=f"del_m_{sample.uuid}"))
    return keyboard


async def delete_branding_sample_menu(to_user: User) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    saved_samples = await Watermark.filter(user=to_user)
    for sample in saved_samples:
        keyboard.add(InlineKeyboardButton(text=sample.title, callback_data=f"del_b_{sample.uuid}"))
    return keyboard


async def delete_marking_sample_confirm_menu(id: UUID4) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    sample = await Contour.get_by_id(id=id)

    keyboard.add(InlineKeyboardButton(text=texts.delete_sample_menu_confirm(sample_name=sample.title), callback_data=f"conf_del_m_{sample.uuid}"))
    keyboard.add(InlineKeyboardButton(text=texts.back_to_main_menu, callback_data="del_marking_menu"))
    return keyboard


async def delete_branding_sample_confirm_menu(id: UUID4) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    sample = await Watermark.get_by_id(id=id)

    keyboard.add(InlineKeyboardButton(text=texts.delete_sample_menu_confirm(sample_name=sample.title), callback_data=f"conf_del_b_{sample.uuid}"))
    keyboard.add(InlineKeyboardButton(text=texts.back_to_main_menu, callback_data="del_branding_menu"))
    return keyboard


# def marking_menu() -> InlineKeyboardMarkup:
#     keyboard = InlineKeyboardMarkup()
#     marking_app = WebAppInfo("https://tgweb.cherry4xo.ru")
#     keyboard.add(InlineKeyboardButton(text=texts.create_sample))
#     keyboard.add(InlineKeyboardButton(text=texts.round_samples, callback_data=f"round_samples"))
#     # keyboard.add(InlineKeyboardButton(text=texts.back_to_samples_menu, callback_data=f"back_samples"))
#     return keyboard


# def branding_menu() -> InlineKeyboardMarkup:
#     keyboard = InlineKeyboardMarkup()
#     marking_app = WebAppInfo("https://tgweb.cherry4xo.ru")
#     keyboard.add(InlineKeyboardButton(text=texts.create_sample))
#     keyboard.add(InlineKeyboardButton(text=texts.samples_text, callback_data=f"watermark_samples"))

#     return keyboard


async def round_samples_menu(to_user: User) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    saved_samples = await Contour.filter(user=to_user)
    for sample in saved_samples:
        keyboard.add(InlineKeyboardButton(text=sample.title, callback_data=f"round_sample_{sample.uuid}"))
    # keyboard.add(InlineKeyboardButton(text=texts.back_to_samples_menu, callback_data=f"back_round_samples"))
    return keyboard


async def watermark_pictures_menu(to_user: User) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    saved_pictures = await WatermarkPicture.filter(user=to_user)
    for picture in saved_pictures:
        keyboard.add(InlineKeyboardButton(text=picture.title, callback_data=f"watermark_picture_{str(picture.id)}"))
    keyboard.add(InlineKeyboardButton(text=texts.add_new_watermark, callback_data=f"watermark_new_picture"))
    keyboard.add(InlineKeyboardButton(text=texts.delete_picture, callback_data=f"delete_picture"))
    # keyboard.add(InlineKeyboardButton(text=texts.back_to_samples_menu, callback_data=f"back_watermark_samples"))
    return keyboard


async def delete_pictures_menu(to_user: User) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    saved_pictures = await WatermarkPicture.filter(user=to_user)
    for picture in saved_pictures:
        keyboard.add(InlineKeyboardButton(text=picture.title, callback_data=f"del_p_{str(picture.id)}"))
    keyboard.add(InlineKeyboardButton(text=texts.back_to_samples_menu, callback_data=f"pictures_menu"))
    return keyboard


async def delete_pictures_confirm_menu(picture_id: id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    picture = await WatermarkPicture.get_by_id(id=picture_id)
    keyboard.add(InlineKeyboardButton(text=texts.delete_picture_menu_confirm(picture_name=picture.title), callback_data=f"conf_del_p_{picture.id}"))
    keyboard.add(InlineKeyboardButton(text=texts.back_to_main_menu, callback_data="delete_picture"))
    return keyboard


async def watermark_samples_menu(to_user: User, picture_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    saved_samples = await Watermark.filter(user=to_user)
    for sample in saved_samples:
        keyboard.add(InlineKeyboardButton(text=sample.title, callback_data=f"w_s_{sample.uuid}_{picture_id}"))
    keyboard.add(InlineKeyboardButton(text=texts.back_to_samples_menu, callback_data=f"back_watermark_pictures"))
    return keyboard


def tariff() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=texts.price(10, 250), callback_data=f"tariff_10_250"))
    keyboard.add(InlineKeyboardButton(text=texts.price(50, 500), callback_data=f"tariff_50_500"))
    keyboard.add(InlineKeyboardButton(text=texts.price(100, 1350), callback_data=f"tariff_100_1350"))
    keyboard.add(InlineKeyboardButton(text=texts.price(150, 1500), callback_data=f"tariff_150_1500"))
    keyboard.add(InlineKeyboardButton(text=texts.check_payment, callback_data="check_payment"))

    return keyboard
    
