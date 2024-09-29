import requests
from bs4 import BeautifulSoup
import requests
import json
from config import CHANNEL_ID, BOT_TOKEN

import logging




GOOGLE_AI_STUDIO_API = "AIzaSyCQ6dSd3Di9BtgMTwk20xnlWZyu2UXb4xU"

def perser_protothema(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    img_tag = soup.find('img', class_='attachment-s_post size-s_post wp-post-image')
    img_url = img_tag.get('src') if img_tag and hasattr(img_tag, 'get') else None


    title_tag = soup.find('div', class_='title title--noDot')
    if title_tag:
        title = title_tag.get_text()
    else:
        title = "Заголовок не найден"

    article_content = []
    for p in soup.select('#site-content > article > div > div.smart-grid > div.post-content.mb-25 p'):
        article_content.append(p.get_text())

    article_top_info_tag = soup.find('div', class_='articleTopInfo')
    if article_top_info_tag:
        article_top_info = article_top_info_tag.get_text()
    else:
        article_top_info = "Информация не найдена"

    article_top_info = "\n".join(article_content)


    content_tag = soup.find('div', class_='cnt')
    if content_tag:
        content = content_tag.get_text()
    else:
        content = "Содержание не найдено"
  

    return img_url, title, article_top_info, content




























































# url = "https://www.naftemporiki.gr/kosmos/1767313/live-deyteri-apopeira-dolofonias-kata-tramp-o-58chronos-drastis-ta-kinitra-kai-osa-fernoyn-sto-fos-oi-ereynes/"
url = "https://www.naftemporiki.gr/finance/economy/1767681/ielka-poso-kostizei-to-kalathi-toy-soyper-market-stin-ellada-sygkritika-me-alles-eyropaikes-chores-pinakes/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Извлечение картинки
img_tag = soup.find('img', class_='attachment-s_post size-s_post wp-post-image')
img_url = img_tag.get('src') if img_tag and hasattr(img_tag, 'get') else None

print("Image URL:", img_url)

# Извлечение заголовка
title_tag = soup.find('title')
if title_tag:
    title = title_tag.get_text()
else:
    title = "Заголовок не найден"

# print("Title:\n", title)

# Извлечение содержания статьи
article_content = []
for p in soup.select('#site-content > article > div > div.smart-grid > div.post-content.mb-25 p'):
    article_content.append(p.get_text())
# Объединение параграфов в одно содержание
content = "\n".join(article_content)

# print("Article content:\n", content)


def send_request_to_google(title, content):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyCQ6dSd3Di9BtgMTwk20xnlWZyu2UXb4xU'
    headers = {'Content-Type': 'application/json'}
    
    # Формирование данных для отправки
    data = {
        "system_instruction":
            {
              "parts": [
                  {"text": "ты опытный журналист, перепеши для поста в twitter, "},
                  {"text": "тебе запрещено менять смысл исходного текста "},
                  {"text": "строго без emoji. в твоем ответе должен быть жирный заголовок [<b>bold</b>] отделенный от основного текста и в конце hashtag"}
                  ]
              
            },
        "contents": [
            {
                "parts": [
                    {"text": title},
                    {"text": content}
                ]
            }
        ]
    }
    
    # Отправка POST-запроса
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # Вывод результата
    # print("Статус код:", response.status_code)
    # print("Ответ:", response.json())


    return response


# Пример использования
resp = send_request_to_google(title, content)
# print(resp.json())
def extract_text_from_response(response_data):
    try:
        text = response_data['candidates'][0]['content']['parts'][0]['text']
        print(text)
        return text
    except (KeyError, IndexError) as e:
        logging.error(f"Ошибка при извлечении текста из ответа: {e}")
        return None
    
extracted_text = extract_text_from_response(resp.json())

def sent_message_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {
        "chat_id": CHANNEL_ID,
        "photo": img_url,
        "caption": extracted_text,
        "parse_mode": "MarkdownV2"
    }
    
    requests.post(url, data=data)


sent_message_to_telegram(resp.json())

