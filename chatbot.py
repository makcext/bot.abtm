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
# BOT_TOKEN = "6735927791:AAEtA7jjgR7WJXL0ZW1tmt-Dpd42ORzMZxA"
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
    time_period_message = "ola kala bot ->  \ndialekse mia poikilia:"
    reply_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    reply_markup.add(
        telebot.types.InlineKeyboardButton(text="Small", callback_data="15"),
        telebot.types.InlineKeyboardButton(text="Big", callback_data="20"),
    )
    sent_message = bot.send_message(message.chat.id, time_period_message, reply_markup=reply_markup)
    time_period_message_id = sent_message.message_id


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global num_posts
    top_posts = []
    if call.data == "15" or call.data == "20":
        num_posts = int(call.data)
        bot.send_message(chat_id=call.message.chat.id, text="Λήψη...")
        time.sleep(2)
        top_posts = reddit.subreddit("Greece").top(time_filter="day", limit=num_posts)
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
                    time.sleep(1.5)

                elif 'reddit.com/gallery' in post.url:
                    url_list = []
                    for _, item_info in post.media_metadata.items():
                        if 's' in item_info:
                            image_url = item_info['s']['u']
                            url_list.append(image_url)

                    if url_list:
                        bot.send_media_group(chat_id=call.message.chat.id, media=[telebot.types.InputMediaPhoto(media) for media in url_list])
                        # print("URLs extracted from the gallery:")
                        # for url in url_list:
                        #     print(url)
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
                    time.sleep(1)
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