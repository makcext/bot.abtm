from tokenize import group
import praw
import telebot
import pickle
import time
import requests
import random
import logging
from io import BytesIO

# Constants
# CHANNEL_ID = "-1001715730728" #local
CHANNEL_ID = "@ola_kala" #prod
CLIENT_ID = "YJ85gCYgTVVMtcdsY4jzcw"
CLIENT_SECRET = "hiPHteFqF5Xb9OUQNBsYfda71L-CxQ"
USER_AGENT = "myapp/1.0"
BOT_TOKEN = "6105348307:AAGK-UaRDXrFdZhYSP_t8gY4aYjbDO5SN6s" #group bot

LAST_TIMESTAMP_FILE = "last_timestamp.txt"
DELAY_MIN = 100
DELAY_MAX = 450

# Map link flair text to tag
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

try:
    with open("sent_post_ids.pkl", "rb") as file:
        sent_post_ids = pickle.load(file)
except FileNotFoundError:
    sent_post_ids = set()

def download_posts_from_subreddit(last_timestamp):
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )

    # subreddit = reddit.subreddit("greece")
    subreddit = reddit.subreddit("greece")
    posts = subreddit.new(limit=3)
    downloaded_posts = []
    new_last_timestamp = last_timestamp

    for post in posts:
        post_timestamp = post.created_utc
        if post_timestamp > last_timestamp:
            downloaded_posts.append(post)
            new_last_timestamp = max(new_last_timestamp, post_timestamp)

    return downloaded_posts, new_last_timestamp

def save_last_timestamp(last_timestamp):
    with open(LAST_TIMESTAMP_FILE, "wb") as file:
        pickle.dump(last_timestamp, file)

def load_last_timestamp():
    try:
        with open(LAST_TIMESTAMP_FILE, "rb") as file:
            last_timestamp = pickle.load(file)
    except FileNotFoundError:
        last_timestamp = 0

    return last_timestamp

def process_posts(downloaded_posts, bot):
    global sent_post_ids
    for post in downloaded_posts:
        if post.title in sent_post_ids:
            logging.info("Skipping post: already sent")
            continue

        if post.link_flair_text in [":zz_question: ερωτήσεις/questions"] or post.is_self:
            logging.info("Skipping post: question or self post")
            print(post.link_flair_text)
            continue

        tag = FLAIR_TO_TAG.get(post.link_flair_text, "")
        photo_caption = f"{post.title} {tag}"
        message_caption = tag
        group_photo_caption = f"{post.title} {tag}"

        try:
            if post.url.endswith((".jpg", ".jpeg", ".png", ".gif")):
                
                photo = requests.get(post.url).content
                bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=photo,
                    caption=photo_caption
                )
                
                logging.info("photo sent")
                sent_post_ids.add(post.title)
                time.sleep(1.5)

            elif 'reddit.com/gallery' in post.url:
                    
                   
                    url_list = []
                    for _, item_info in post.media_metadata.items():
                        if 's' in item_info:
                            image_url = item_info['s']['u']
                            url_list.append(image_url)

                    if url_list:
                        media_group = [telebot.types.InputMediaPhoto(url_list[0], caption=group_photo_caption)]
                        media_group.extend([telebot.types.InputMediaPhoto(media) for media in url_list[1:]])
                        bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
                        
                        logging.info("group photo sent")
                        sent_post_ids.add(post.title)

                    else:
                        logging.info("No URLs to extract")

                    time.sleep(1.5)

            elif post.url.startswith("https://"):
                
                bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=f"<a href='{post.url}'>◉  </a>{message_caption} ",
                    parse_mode="HTML",
                    disable_web_page_preview=False
                )
                
                logging.info(f"link sent with tag: {tag}")
                sent_post_ids.add(post.title)
                time.sleep(1.5)

            with open("sent_post_ids.pkl", "wb") as file:
                pickle.dump(sent_post_ids, file)    

        except Exception as e:
            logging.error(f"Error sending message or photo or groupPhoto: {e}")



def main():
    last_timestamp = load_last_timestamp()
    downloaded_posts, new_last_timestamp = download_posts_from_subreddit(last_timestamp)
    bot = telebot.TeleBot(BOT_TOKEN)
    process_posts(downloaded_posts, bot)
    save_last_timestamp(new_last_timestamp)

if __name__ == "__main__":
    while True:
        main()
        delay = random.randint(DELAY_MIN, DELAY_MAX)
        logging.info(f"Sleeping for {delay} seconds")
        time.sleep(delay)