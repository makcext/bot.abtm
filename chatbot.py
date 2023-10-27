import praw
import telebot
import pickle
import time
import requests
import random
import logging
from io import BytesIO
from telebot import types

# Constants
# CHANNEL_ID = "-1001715730728"
CLIENT_ID = "YJ85gCYgTVVMtcdsY4jzcw"
CLIENT_SECRET = "hiPHteFqF5Xb9OUQNBsYfda71L-CxQ"
USER_AGENT = "myapp/1.0"
BOT_TOKEN = "6735927791:AAEtA7jjgR7WJXL0ZW1tmt-Dpd42ORzMZxA"
# BOT_TOKEN = "6922909929:AAFklaLqTBQKpctjkzpJwCV42fFCXefq-F0"
LAST_TIMESTAMP_FILE = "last_timestamp.txt"
DELAY_MIN = 10
DELAY_MAX = 15


bot = telebot.TeleBot(BOT_TOKEN)




reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
)

time_period = ""
num_posts = 0
time_period_message_id = None

FLAIR_TO_TAG = {
    ":zz_funny:  αστείο/funny": "#funny",
    ":zz_personal: προσωπικά/personal": "#personal",
    ":zz_travel: travel/τουρισμός": "#travel",
    ":zz_politics: πολιτική/politics": "#politics",
    ":zz_society: κοινωνία/society": "#society",
    ":zz_culture: πολιτιστικά/culture": "#culture",
    ":zz_economy: οικονομία/economy": "#economy",
    ":zz_science: επιστήμη/science": "#science",
    ":zz_sports: αθλητισμός/sports": "#sports",
    ":zz_education: εκπαίδευση/education": "#education",
    ":zz_history: ιστορία/history": "#history",
    ":zz_technology: τεχνολογία/technology": "#technology",
    ":zz_entertainment: ψυχαγωγία/entertainment": "#entertainment",
    ":zz_food: κουζίνα/food": "#food"
}
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@bot.message_handler(commands=['start'])
def start(message):
    global time_period_message_id
    time_period_message = "ola kala bot ->  \nΔιαλέξτε μια περίοδο:"
    reply_markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    reply_markup.add(
        telebot.types.InlineKeyboardButton(text="Σήμερα", callback_data="day"),
        telebot.types.InlineKeyboardButton(text="Εβδομάδα", callback_data="week"),
        # telebot.types.InlineKeyboardButton(text="Μήνα", callback_data="month")
    )
    sent_message = bot.send_message(message.chat.id, time_period_message, reply_markup=reply_markup)
    time_period_message_id = sent_message.message_id


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global time_period, num_posts, time_period_message_id
    top_posts = []
    if call.data == "day" or call.data == "week" or call.data == "month":
        time_period = call.data
        num_posts_message = "Διαλέξτε μια ποσότητα:"
        reply_markup = telebot.types.InlineKeyboardMarkup(row_width=3)
        reply_markup.add(
            telebot.types.InlineKeyboardButton(text="5", callback_data="5"),
            telebot.types.InlineKeyboardButton(text="10", callback_data="10"),
            telebot.types.InlineKeyboardButton(text="15", callback_data="15")
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=time_period_message_id, text=num_posts_message, reply_markup=reply_markup)
    elif call.data == "5" or call.data == "10" or call.data == "15":
        num_posts = int(call.data)
        bot.send_message(chat_id=call.message.chat.id, text=f"Λήψη {num_posts} κορυφαίων αναρτήσεων από το @ola_kala")
        time.sleep(2)
        if time_period == "day":
            top_posts = reddit.subreddit("Greece").top(time_filter="day", limit=num_posts)
        elif time_period == "week":
            top_posts = reddit.subreddit("Greece").top(time_filter="week", limit=num_posts)
        # elif time_period == "month":
        #     top_posts = reddit.subreddit("Greece").top(time_filter="month", limit=num_posts)
        for post in top_posts:
            if post.link_flair_text in [":zz_question: ερωτήσεις/questions", None] or post.is_self:
                logging.info("Skipping post: question or self post")
                continue

            tag = FLAIR_TO_TAG.get(post.link_flair_text, "")
            photo_caption = f"{post.title} {tag}"
            message_caption = tag

            try:
                if post.url.endswith((".jpg", ".jpeg", ".png", ".gif")):
                    photo = requests.get(post.url).content
                    bot.send_photo(
                        chat_id=call.message.chat.id,
                        photo=photo,
                        caption=photo_caption
                    )
                    logging.info("photo sent")
                elif post.url.startswith("https://"):
                    bot.send_message(
                        chat_id=call.message.chat.id,
                        text=f"<a href='{post.url}'>◉  </a>{message_caption} ",
                        parse_mode="HTML",
                        disable_web_page_preview=False
                    )
                    logging.info(f"link sent with tag: {tag}")
                    time.sleep(1.5)
            except Exception as e:
                logging.error(f"Error sending message or photo: {e}")

        # restart_markup = telebot.types.InlineKeyboardMarkup()
        # restart_markup.add(telebot.types.InlineKeyboardButton(text="Έξοδος", callback_data="restart"))
        bot.send_message(chat_id=call.message.chat.id, text="---------- \n/start \n----------" )
    # elif call.data == "restart":
    #     time_period = ""
    #     num_posts = 0
    #     bot.send_message(chat_id=call.message.chat.id, text="Πάτα το /start")


bot.polling()







