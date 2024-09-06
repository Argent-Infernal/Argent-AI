from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.utils import markdown

from app.database.requests import db_get_balance, db_get_free_messages

router = Router()

async def profile_command_handler(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    text = markdown.text(
        "Ваш профиль:",
        f"Баланс: {markdown.bold(str(await db_get_balance(tg_id)))} ₽",
        f"Бесплатных запросов для {markdown.bold("GPT-3.5 Turbo")}: {markdown.bold(str(await db_get_free_messages(tg_id)))} ",
        f"Для пополнения баланса напишите: {markdown.bold("/pay")}",
        sep="\n",
    )

    await message.answer(text, parse_mode= ParseMode.MARKDOWN_V2)
    await state.clear()


@router.callback_query()
async def callbackQuery(callback: CallbackQuery, state: FSMContext):
    pass
