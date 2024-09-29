import requests
from config import CHANNEL_ID, BOT_TOKEN, FLAIR_TO_TAG

import logging

def send_photo_message_to_telegram(img_url, extracted_text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {
        "chat_id": CHANNEL_ID,
        "photo": img_url,
        "caption": extracted_text,
        "parse_mode": "Markdown"
    }
    
    requests.post(url, data=data)
    print("photo sent")

def send_message_to_telegram_link(post, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": f"<a href='{post.url}'>◉  </a>{caption}",
        "parse_mode": "HTML",
        "disable_web_page_preview": False
        # "parse_mode": "MarkdownV2"
        
    }
    
    requests.post(url, data=data)
    print("link sent")



    
