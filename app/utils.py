from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import httpx
from tiktoken import get_encoding
from config import CHATGPT_MODELS
from app.database.requests import db_get_free_messages, db_add_free_messages, db_get_balance, db_add_balance

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("AI_TOKEN"),
                     base_url="https://api.proxyapi.ru/openai/v1",
                     #http_client = httpx.AsyncClient(
                         #proxies = os.getenv('PROXY'),
                         #transport = httpx.HTTPTransport(local_address = "0.0.0.0")
                     )#)

async def getCost(model,data):
    baseCost = 0
    for models in CHATGPT_MODELS:
        if model == models["model"]:
            baseCost = models["cost"]

            if data:
                if data["model"] == "dall-e-2":
                    if data["inlineData"][0] == "256x256":
                        baseCost = 5.10
                    elif data["inlineData"][0] == "512x512":
                        baseCost = 5.69
                    elif data["inlineData"][0] == "1024x1024":
                        baseCost = 6.26
                elif data["model"] == "dall-e-3":
                    if data["inlineData"][0] == "1024x1024":
                        baseCost = 12.02
                    elif data["inlineData"][0] == "1792x1024":
                        baseCost = 23.54
                    elif data["inlineData"][0] == "1024x1792":
                        baseCost = 23.54

    return baseCost


async def getTypeText(type):
    type = "Генерация текста и ответов на вопросы"

    if type == "img":
        type = "Генерация изображений"
    return type

async def getModelTable(model):
    modelTable = []

    for models in CHATGPT_MODELS:
        if models["model"] == model:
            modelTable = models
            break

    return modelTable

async def gpt(question, modelData, tg_id):

    model = modelData["model"]

    modelTable = await getModelTable(model)

    if not modelTable:
        return ["Ошибка выбора модели", ""]
    
    cost = await getCost(model, modelData)
    type = modelTable["type"]

    money = await db_get_balance(tg_id)
    free_messages = await db_get_free_messages(tg_id)

    if model == "gpt-3.5-turbo-0125":
        if free_messages <= 0:
            if money < cost:
                return ["У вас закончились бесплатные вопросы, пополните баланс",""]
    else:
        if money < cost:
            return ["Недостаточно средств, пополните баланс",""]
    
    encoding_name = "cl100k_base"
    if model == "gpt-4o":
        encoding_name = "o200k_base"

    encoding = get_encoding(encoding_name)
    num_tokens = len(encoding.encode(question))

    if num_tokens >= 500:
        return ["Вы превысили количество символов в сообщении, переформулируйте вопрос.",""]
    else:
        ret = []
        if type == 'text':

            response = await client.chat.completions.create(
                messages = [{
                    "role": "user",
                    "content": str(question)
                }],
                model = str(model),
                max_tokens = 1000,
            )

            ret = [response.choices[0].message.content,""]

        elif type == "img":
            pass
            size = "256x256"

            if model == "dall-e-3":
                size = "1024x1024"

            response = await client.images.generate(
                model=str(model),
                prompt=question,
                size=size, # 1024x1024, 1024x1792, 1792x1024
                quality="standard", # standard, hd
                n=1,
            )
            
            image_url = response.data[0].url

            ret = ["img",image_url]
        
        if model == "gpt-3.5-turbo-0125":
            if free_messages > 0:
                await db_add_free_messages(tg_id,-1)
            else:
                await db_add_balance(tg_id, -cost)
        else:
            await db_add_balance(tg_id, -cost)

        return ret
