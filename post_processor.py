import logging
import asyncio
from telebot.types import InputMediaPhoto
from config import CHANNEL_ID, FLAIR_TO_TAG
from data_manager import load_sent_post_ids, save_sent_post_ids
from notify import  send_message_to_telegram_link, send_photo_message_to_telegram
from parsers.parser_thepressproject import parser_thepressproject
from parsers.parser_protothema import parser_protothema

send_post_ids = load_sent_post_ids()

async def process_posts(downloaded_posts, bot):
    global send_post_ids
    for post in downloaded_posts:
        
        if post.title in send_post_ids:
            logging.info("Skipping post: already sent")
            continue

        if post.link_flair_text in [":zz_question: ερωτήσεις/questions"] or post.is_self:
            logging.info("Skipping post: question or text post")
            continue

        tag = FLAIR_TO_TAG.get(post.link_flair_text, "")
        caption = f"{post.title} {tag}"

        try:
            if hasattr(post, 'is_gallery') and post.is_gallery:
                await process_gallery(post, bot, caption)
            elif post.url.endswith((".jpg", ".jpeg", ".png", ".gif")):
                await process_single_image(post, caption)
            elif post.url.startswith("https://"):
                await post_link_processing(post)

            send_post_ids.append(post.title)
            send_post_ids = send_post_ids[-15:]  # Сохраняем только последние 15 идентификаторов
            save_sent_post_ids(send_post_ids)

            await asyncio.sleep(1.5)

        except Exception as e:
            logging.error(f"Error sending post: {e}")
            logging.error(f"Post title: {post.title}, {post.id}")
            logging.error(f"Post URL: {post.url}")






async def process_gallery(post, bot, caption):
    media_group = []
    for item in post.gallery_data['items']:
        media_id = item['media_id']
        media_url = post.media_metadata[media_id]['s']['u']
        media_group.append(InputMediaPhoto(media_url))

        if len(media_group) == 10:
            media_group[0].caption = caption
            await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
            logging.info("Gallery sent")
            break  # Прерываем цикл после отправки 10 медиафайлов

async def process_single_image(post, caption):
    caption = caption
    img_url = post.url
    send_photo_message_to_telegram(img_url, caption)

    logging.info("Photo send")



async def post_link_processing(post):
    print(post.url)
    if post.url.startswith("https://naftemporiki.gr/") or post.url.startswith("https://www.naftemporiki.gr/"):
        pass
    elif post.url.startswith("https://protothema.gr") or post.url.startswith("https://www.protothema.gr"):
        tag = FLAIR_TO_TAG.get(post.link_flair_text, "")
        parser_protothema(post.url, tag)
        return
    elif post.url.startswith("https://thepressproject.gr/") or post.url.startswith("https://www.thepressproject.gr/"):
        tag = FLAIR_TO_TAG.get(post.link_flair_text, "")
        parser_thepressproject(post.url, tag)
        return
    else:
        await process_link(post)


async def process_link(post):
    tag = FLAIR_TO_TAG.get(post.link_flair_text, "")
    caption = f"{tag}"
    send_message_to_telegram_link(post, caption)






