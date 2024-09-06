import os

from aiogram import F
from aiogram.filters import CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import PreCheckoutQuery

from app.database.requests import db_add_balance,db_get_user_id

class PaymentsState(StatesGroup):
    amount = State()
    pay = State()

async def add_money_handler(message: Message, state: FSMContext,command: CommandObject):
    args = command.args.split(" ")

    tg_id = await db_get_user_id(args[0])
    if not tg_id: 
        await message.answer("Такого пользователя в базе нет")
        return
    
    await db_add_balance(tg_id, int(args[1]))
    await message.answer("Деньги успешно выданы")

async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True, error_message="Сейчас нельзя совершить оплату")

async def success_payment_handler(message: Message, state: FSMContext):  
    if message.successful_payment.invoice_payload == "pay":
        
        amount = message.successful_payment.total_amount
        await db_add_balance(message.from_user.id, amount)
        await message.answer(f"Вы пополнили баланс на {amount}")
        await state.clear()

async def pay_command_handler(message: Message, state: FSMContext):
    await state.clear()

    await state.set_state(PaymentsState.amount)
    await message.answer("Напишите в чат сумму для пополнения, без копеек (минимум 60 рублей)")

async def amountReply(message:Message,state:FSMContext):
    amount = message.text 
    bool = False

    try:
        amount = int(amount)
        bool = True
    except:
        bool = False

    if amount < 60:
        await message.answer("Сумма должна быть больше 60 рублей.")
        return

    if bool:
        await state.update_data(amount = amount)
        await sendPayment(message,state)
        #await sendPayment(message,state, amount)
    else:
        await message.answer("Неправильный ввод числа")


async def sendPayment(message: Message, state: FSMContext):
    await state.set_state(PaymentsState.pay)
    data = await state.get_data()

    amount = str(data["amount"])
    amountFloat = int(str(amount) + "00")

    await message.answer_invoice(
        title = "Пополнение баланса",
        description="Пополнение баланса",
        payload="pay",
        provider_token=os.getenv("YOOKASSA_KEY"),
        currency="RUB",
        start_parameter="user_payments",
        #need_email = True,
        #send_email_to_provider = True,
        #     "receipt": {
        #         "items": {
        #             "description": "Пополнение баланса",
        #             "quantity": "1",
        #             "amount": {
        #                 "value": f"{amount}.00",
        #                 "currency": "RUB"
        #             }, 
        #             "vat_code": "1"
        #         }#,
        #         #"email": str(email)
        #     }
        # },
        prices=[{
            "label": "Руб",
            "amount": amountFloat
        }]
    )
