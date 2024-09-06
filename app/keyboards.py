import os
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import CHATGPT_MODELS

async def inline_models():
    keyboard = InlineKeyboardBuilder()
    for models in CHATGPT_MODELS:

        keyboard.add(InlineKeyboardButton(text = models["printName"], callback_data = "chatgpt_init_"+models["model"]))

    return keyboard.adjust(2).as_markup()

async def inline_data(data):

    keyboard = InlineKeyboardBuilder()

    for models in CHATGPT_MODELS:
        if models["model"] == data["model"]:
            for dataValue in models["inlineData"][data["inlineStage"]-1]["values"]:
                keyboard.add(InlineKeyboardButton(text = dataValue, callback_data = "chatgpt_data_" + models["model"] + "_" + dataValue))
            break

    return keyboard.adjust(2).as_markup()

async def reply_user(user_id):
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(KeyboardButton(text = "Мой профиль"))
    keyboard.add(KeyboardButton(text = "Помощь"))

    if (user_id == int(os.getenv('ADMIN_ID')) ):
        keyboard.add(KeyboardButton(text = "Админ меню"))

    return keyboard.adjust(3).as_markup(resize_keyboard=True, input_field_placeholder="Выберите что вам нужно:", one_time_keyboard=True)

async def inline_admin():
    pass