import os
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram.fsm.context import FSMContext

import app.payments as payments
from app.chatgpt import callback_gpt_handler, finish_gpt_handler, chatgpt_command_handler

#handlers
from app.admin import admin_command_handler
from app.main_commands import help_command_handler
from app.profile import profile_command_handler
from aiogram.exceptions import TelegramForbiddenError
#DataBase
from app.database.requests import db_set_user

#States
from app.payments import PaymentsState
from app.chatgpt import ChatGPTState

router = Router()

@router.message(Command("start"))
async def com(message: Message, state: FSMContext):
    try:
        await db_set_user(message.from_user.id, message.from_user.username)
        await help_command_handler(message, state)
    except TelegramForbiddenError:
        print("Attention please! The user has blocked the bot. I can't send anything to them")

@router.message(Command("help"))
async def com(message: Message, state: FSMContext):
    await help_command_handler(message,state)

@router.message(Command("chatgpt"))
async def com(message: Message, state: FSMContext):
    await chatgpt_command_handler(message, state)

@router.message(Command("addmoney"))
async def com(message: Message, state: FSMContext, command: CommandObject):
    await payments.add_money_handler(message, state, command)

@router.message(Command("pay"))
async def com(message: Message, state: FSMContext):
    await payments.pay_command_handler(message, state)

@router.callback_query()
async def callbackQuery(callback: CallbackQuery, state: FSMContext):

    callbackMessage = callback.data.split("_")

    if callbackMessage[0] == "chatgpt":

        await callback_gpt_handler(callback, state, callbackMessage)

@router.message(F.text)
async def reply_user(message: Message, state: FSMContext):

    if message.text == "Мой профиль":
        await state.clear()
        await profile_command_handler(message,state)
        return
    
    elif message.text == "Помощь":
        await state.clear()
        await help_command_handler(message, state)
        return
    
    elif (message.from_user.id == int(os.getenv('ADMIN_ID')) ) and (message.text == "Админ меню"):
        await state.clear()
        await admin_command_handler(message,state)
        return

    if await state.get_state() == ChatGPTState.textGeneration:
        await message.answer("Подождите, ИИ Генерирует ответ.")
        return

    if await state.get_state() == ChatGPTState.textInput:
        await finish_gpt_handler(message,state)
        return

    if await state.get_state() == PaymentsState.amount:
        await payments.amountReply(message,state)
        return

@router.pre_checkout_query()
async def com(pre_checkout_query: PreCheckoutQuery):
    await payments.pre_checkout_handler(pre_checkout_query)

@router.message(F.successful_payment)
async def com(message: Message, state: FSMContext):
    await payments.success_payment_handler(message, state)