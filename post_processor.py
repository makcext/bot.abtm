import logging
import asyncio
from telebot.types import InputMediaPhoto
from config import CHANNEL_ID, FLAIR_TO_TAG
from data_manager import load_sent_post_titles, save_sent_post_titles
from notify import  send_message_to_telegram_link, send_photo_message_to_telegram
from parsers.parser_thepressproject import parser_thepressproject
from parsers.parser_protothema import parser_protothema

# send_post_ids = load_sent_post_titles()
# Инициализируем sent_post_titles как множество
sent_post_titles = load_sent_post_titles()
# Список подстрок, которые должны быть в URL, чтобы пост не пропускался
required_substrings = ["facebook.com", "https://open.spotify.com", "www.cinemagazine.gr" ]

async def process_posts(downloaded_posts, bot):
    global sent_post_titles  # Используем множество вместо списка
    for post in downloaded_posts:
        if should_skip_post(post):
            continue

        tag = FLAIR_TO_TAG.get(post.link_flair_text, "")
        caption = f"{post.title} {tag}"

        try:
            await process_post_content(post, bot, caption)

            sent_post_titles.add(post.title)  # Добавляем заголовок поста в множество
            save_sent_post_titles(sent_post_titles)  # Сохраняем обновленное множество

            await asyncio.sleep(1.5)

        except Exception as e:
            logging.error(f"Ошибка при отправке поста '{post.title}': {e}")
            logging.error(f"ID поста: {post.id}")
            logging.error(f"URL поста: {post.url}")

def should_skip_post(post):
    """Проверяет, следует ли пропустить текущий пост."""
    title = post.title[:24]  # Ограничиваем длину заголовка до 24 символов
    if is_question_or_text_post(post):
        logging.info(f"skip post: вопрос или текстовый пост '{title}'")
        return True
    if is_unwanted_url(post.url):
        logging.info(f"skip post: URL содержит нежелательные подстроки '{title}'")
        return True
    if post.title in sent_post_titles:
        logging.info(f"skip post: уже отправлен ранее '{title}'")
        return True
    return False

def is_unwanted_url(url):
    """Проверяет, содержит ли URL нежелательные подстроки."""
    return any(substring in url for substring in required_substrings)

def is_question_or_text_post(post):
    """Проверяет, является ли пост вопросом или текстовым постом."""
    return post.link_flair_text in [":zz_question: ερωτήσεις/questions"] or post.is_self

async def process_post_content(post, bot, caption):
    """Обрабатывает содержимое поста в зависимости от его типа."""
    if hasattr(post, 'is_gallery') and post.is_gallery:
        await process_gallery(post, bot, caption)
    elif post.url.endswith((".jpg", ".jpeg", ".png", ".gif")):
        await process_single_image(post, caption)
    elif post.url.startswith("https://"):
        # await post_link_processing(post)
        await process_link(post)


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



# async def post_link_processing(post):
#     print(post.url)
#     if post.url.startswith("https://naftemporiki.gr/") or post.url.startswith("https://www.naftemporiki.gr/"):
#         pass
#     # elif post.url.startswith("https://protothema.gr") or post.url.startswith("https://www.protothema.gr"):
#         # tag = FLAIR_TO_TAG.get(post.link_flair_text, "")
#         # parser_protothema(post.url, tag)
#         # return
#     elif post.url.startswith("https://thepressproject.gr/") or post.url.startswith("https://www.thepressproject.gr/"):
#         # tag = FLAIR_TO_TAG.get(post.link_flair_text, "")
#         # parser_thepressproject(post.url, tag)
#         # return
#         pass
#     else:
#         await process_link(post)


async def process_link(post):
    tag = FLAIR_TO_TAG.get(post.link_flair_text, "")
    caption = f"{tag}"
    send_message_to_telegram_link(post, caption)






