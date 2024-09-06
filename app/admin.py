from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
#from app.ai import gpt4
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
#from app.keyboards import inline_models
#from aiogram.enums import ParseMode

#from config import CHATGPT_MODELS, HELP_TEXT

#from app.database.requests import set_user

router = Router()

class AdminPanel(StatesGroup):
    main = State()

async def admin_command_handler(message: Message, state: FSMContext):

    await state.set_state(AdminPanel.main)

    await message.answer("Админ меню")

@router.callback_query()
async def callbackQuery(callback: CallbackQuery, state: FSMContext):
    pass
    # for models in CHATGPT_MODELS:
    #     if callback.data == models[0]:
    #         await state.update_data(model = callback.data)
    #         await state.set_state(ChatGPT.textInput)
    #         await callback.answer("")
    #         await callback.message.edit_text(f"Модель: {models[1]}")
    #         await callback.message.answer("Напишите сообщение")
