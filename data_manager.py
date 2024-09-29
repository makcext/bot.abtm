import json
from config import SENT_POST_IDS_FILE, LAST_TIMESTAMP_FILE

def load_sent_post_ids():
    try:
        with open(SENT_POST_IDS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_sent_post_ids(ids):
    with open(SENT_POST_IDS_FILE, "w") as file:
        json.dump(ids, file, ensure_ascii=False, indent=4)

def save_last_timestamp(last_timestamp):
    with open(LAST_TIMESTAMP_FILE, "w") as file:
        json.dump(last_timestamp, file)

def load_last_timestamp():
    try:
        with open(LAST_TIMESTAMP_FILE, "r") as file:
            last_timestamp = json.load(file)
    except FileNotFoundError:
        last_timestamp = 0
    return last_timestamp