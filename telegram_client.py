from telebot.async_telebot import AsyncTeleBot
from config import BOT_TOKEN

def create_bot():
    if BOT_TOKEN is not None:
        return AsyncTeleBot(BOT_TOKEN)
    return None