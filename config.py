import os
from dotenv import load_dotenv

load_dotenv()

# Constants
CHANNEL_ID = os.getenv("CHANNEL_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

GOOGLE_AI_STUDIO_API = os.getenv("GOOGLE_AI_STUDIO_API")


LAST_TIMESTAMP_FILE = "z-last_timestamp.json"
SENT_POST_IDS_FILE = "z-sent_post_ids.json"
DELAY_MIN = 300
DELAY_MAX = 550

COUNT_OF_POSTS_TO_DOWNLOAD = 5


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