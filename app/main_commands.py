from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.utils import markdown

from app.keyboards import reply_user
from config import CHATGPT_MODELS

router = Router()

async def help_command_handler(message: Message, state: FSMContext):
    text = markdown.text(
        f"Этот бот позволяет вам использовать все прелести {markdown.bold("ChatGPT")}",
        "",
        f"Для новых пользователей есть 10 бесплатных запросов для {markdown.bold("GPT-3.5 Turbo")}",
        "",
        "Для всех остальных моделей либо после истрачивания бесплатных запросов, действуют следующие расценки за один запрос:",
        "",
        "Генерация текста и ответов на вопросы: ",
        f"{markdown.bold("GPT-4o")} {markdown.underline(str(CHATGPT_MODELS[0]["cost"]))} ₽",
        f"{markdown.bold("GPT-4 Turbo")} {markdown.underline(str(CHATGPT_MODELS[1]["cost"]))} ₽",
        f"{markdown.bold("GPT-3.5 Turbo")} {markdown.underline(str(CHATGPT_MODELS[2]["cost"]))} ₽",
        "",
        "Генерация изображений: ",
        f"{markdown.bold("DALL-E 2 Средняя цена")} {markdown.underline(str(CHATGPT_MODELS[3]["cost"]))} ₽",
        f"{markdown.bold("DALL-E 3 Средняя цена")} {markdown.underline(str(CHATGPT_MODELS[4]["cost"]))} ₽",
        "",
        f"Для того чтобы задать вопрос или сгенерировать изображение используйте команду {markdown.bold("/chatgpt")}, затем выберите нужную вам модель",
        "",
        f"Для того чтобы пополнить свой баланс, используйте команду {markdown.bold("/pay")}",
        f"Примечание: Все GPT Принимают максимально 500 и выдают 1000 токенов, изменение этих параметров будет в ближайших обновлениях",
        sep="\n",
    )
    await message.answer(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup = await reply_user(message.from_user.id))
    await state.clear()
