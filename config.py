from tkinter import Text
from emoji import emojize

CHATGPT_MODELS = [
    {
        "model": "gpt-4o",
        "printName": "GPT-4 Omni",
        "cost": 5.54,
        "type": "text",
        "inlineData": []
    },
    {
        "model": "gpt-4-turbo",
        "printName": "GPT-4 Turbo",
        "cost": 10.54,
        "type": "text",
        "inlineData": []
    },
    {
        "model": "gpt-3.5-turbo-0125",
        "printName": "GPT-3.5 Turbo",
        "cost": 1,
        "type": "text",
        "inlineData": []
    },
    {
        "model": "dall-e-2",
        "printName": "DALL-E 2",
        "cost": 5.69,
        "type": "img",
        "inlineData": [
            {
                "type": "size",
                "text": "Выберите разрешение",
                "textEnd": "Разрешение:",
                "values": [
                    "256x256",
                    "512x512",
                    "1024x1024"
                ]
            }
        ]
    },
    {
        "model": "dall-e-3",
        "printName": "DALL-E 3",
        "cost": 12,
        "type": "img",
        "inlineData": [
            {
                "type": "size",
                "text": "Выберите разрешение",
                "textEnd": "Разрешение:",
                "values": [
                    "1024x1024",
                    "1792x1024",
                    "1024x1792"
                ]
            }
        ]
    },
]

# CHATGPT_MODELS = [
#     ["gpt-4o", "GPT-4 Omni", 5.54, "text"],
#     ["gpt-3.5-turbo-0125", "GPT-3.5 Turbo", 1, "text"],
#     ["gpt-4-turbo", "GPT-4 Turbo", 10.54, "text"],
#     ["dall-e-2", "DALL-E 2", 5.69, "img"],
#     ["dall-e-3", "DALL-E 3", 12, "img"],
# ]
            