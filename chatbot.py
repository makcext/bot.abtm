import praw
import telebot
import pickle
import time
import requests
import random
import logging
from io import BytesIO

# Constants
CHANNEL_ID = "-1001715730728"
CLIENT_ID = "YJ85gCYgTVVMtcdsY4jzcw"
CLIENT_SECRET = "hiPHteFqF5Xb9OUQNBsYfda71L-CxQ"
USER_AGENT = "myapp/1.0"
BOT_TOKEN = "6922909929:AAFklaLqTBQKpctjkzpJwCV42fFCXefq-F0"
LAST_TIMESTAMP_FILE = "last_timestamp.txt"
DELAY_MIN = 10
DELAY_MAX = 15


bot = telebot.TeleBot(BOT_TOKEN)




reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
)

user_answers = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    yes_button = telebot.types.InlineKeyboardButton('Yes', callback_data='yes')
    no_button = telebot.types.InlineKeyboardButton('No', callback_data='no')
    markup.add(yes_button, no_button)
    bot.send_message(message.chat.id, "Hello, do you want to see a news?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    chat_id = call.message.chat.id
    if call.data == 'yes':
        bot.answer_callback_query(call.id, "You pressed Yes")
        user_answers[chat_id] = 'yes'
        subreddit = reddit.subreddit("greece")
        for submission in subreddit.hot(limit=random.randint(1, 10)):
            bot.send_message(chat_id, submission.title)
    elif call.data == 'no':
        bot.answer_callback_query(call.id, "You pressed No")
        user_answers[chat_id] = 'no'

bot.polling()




