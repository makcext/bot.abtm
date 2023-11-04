import praw
import telebot
import pickle
import time
import requests
import random
import logging
from io import BytesIO
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
# Constants
BOT_TOKEN = os.getenv("CHAT_BOT_TOKEN")
if BOT_TOKEN is None:
    raise ValueError("Bot token not found. Please set the environment variable CHAT_BOT_TOKEN")


CLIENT_ID = os.getenv("CHAT_CLIENT_ID")
CLIENT_SECRET = os.getenv("CHAT_CLIENT_SECRET")
USER_AGENT = os.getenv("CHAT_USER_AGENT")

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
    time_period_message = "Διάλεξε το μέγεθος της λίστας που θες να λάβεις:"
    reply_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    reply_markup.add(
        telebot.types.InlineKeyboardButton(text="μικρή", callback_data="8"),
        telebot.types.InlineKeyboardButton(text="μεγάλη", callback_data="16"),
    )
    sent_message = bot.send_message(message.chat.id, time_period_message, reply_markup=reply_markup)
    time_period_message_id = sent_message.message_id


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global num_posts
    top_posts = []
    if call.data == "8" or call.data == "16":
        num_posts = int(call.data)
        bot.send_message(chat_id=call.message.chat.id, text="Λήψη...")
        time.sleep(2)
        top_posts = reddit.subreddit("Greece").top(time_filter="day", limit=num_posts)
        for post in top_posts:
            if post.link_flair_text in [":zz_question: ερωτήσεις/questions"] or post.is_self:
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
                    time.sleep(1.7)

                elif 'reddit.com/gallery' in post.url:
                    url_list = []
                    for _, item_info in post.media_metadata.items():
                        if 's' in item_info:
                            image_url = item_info['s']['u']
                            url_list.append(image_url)

                    if url_list:
                        bot.send_media_group(chat_id=call.message.chat.id, media=[telebot.types.InputMediaPhoto(media) for media in url_list])

                    else:
                        print("No URLs to extract")

                    time.sleep(1.5)

                elif post.url.startswith("https://"):
                    bot.send_message(
                        chat_id=call.message.chat.id,
                        text=f"<a href='{post.url}'>◉  </a>{message_caption} ",
                        parse_mode="HTML",
                        disable_web_page_preview=False
                    )
                    logging.info(f"link sent with tag: {tag}")
                    time.sleep(1.6)
            except Exception as e:
                logging.error(f"Error sending message or photo: {e}")
        bot.send_message(chat_id=call.message.chat.id, text="---------- \n/start \n----------" )

while True:
    try:
        bot.polling()
        break  # If bot.polling() succeeds, break the loop
    except requests.exceptions.ReadTimeout:
        print("Timeout occurred, retrying in 5 seconds...")
        time.sleep(5)