from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

import app.utils as utils
from app.keyboards import inline_models, inline_data

from config import CHATGPT_MODELS

class ChatGPTState(StatesGroup):
    image = State()
    modelData = State()
    textInput = State()
    textGeneration = State()

async def chatgpt_command_handler(message: Message, state: FSMContext):
    await state.set_state(ChatGPTState.modelData)
    await message.answer("Выберите модель", reply_markup = await inline_models())

async def callback_gpt_handler(callback: CallbackQuery, state: FSMContext, callbackMessage):
    callbackData = {}

    for models in CHATGPT_MODELS:

        if callbackMessage[2] == models["model"]:

            if callbackMessage[1] == "init":

                callbackData = {
                    "model": models["model"],
                    "type": models["type"],
                    "inlineStage": 0,
                    "inlineData": [],
                }

                await state.update_data(modelData = callbackData)

            else:

                callbackData = await state.get_data()
                callbackData = callbackData["modelData"]
                callbackData["inlineData"].append(callbackMessage[3])
                    
            if not models["inlineData"] or callbackData["inlineStage"] >= len(models["inlineData"]):

                await state.update_data(modelData = callbackData)
                await state.set_state(ChatGPTState.textInput)
                await callback.answer("")

                text = [
                    f"Модель: {models["printName"]}\n",
                    f"Тип модели: {await utils.getTypeText(type)}\n",
                    f"Стоимость одного запроса: {await utils.getCost(models["model"], callbackData)} ₽\n",
                ]

                key = 0
                for data in callbackData["inlineData"]:
                    text.append(f"{models["inlineData"][key]["textEnd"]}: {data}")
                    key = key + 1

                await callback.message.edit_text("".join(text))
                await callback.message.answer("Напишите сообщение")
            else:
                callbackData["inlineStage"] = callbackData["inlineStage"] + 1

                await state.update_data(modelData = callbackData)

                await callback.message.answer(models["inlineData"][callbackData["inlineStage"]-1]["text"], reply_markup = await inline_data(callbackData))

async def finish_gpt_handler(message: Message, state: FSMContext):
    await state.set_state(ChatGPTState.textGeneration)

    data = await state.get_data()

    response = await utils.gpt(message.text, data["modelData"], message.from_user.id)

    if response[0] == "img":
        await message.answer_photo(photo=response[1])
        #await message.answer(str(response[1][0]))
    else:
        await message.answer(response[0])

    await state.set_state(ChatGPTState.textInput)
    