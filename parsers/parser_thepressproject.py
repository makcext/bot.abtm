from ast import Await
from time import sleep
import requests
from bs4 import BeautifulSoup
import requests
import json
from gemini import send_request_to_google, extract_text_from_response
from notify import send_photo_message_to_telegram

def parser_thepressproject(url, tag):
    print("this is parser_thepressproject")
    
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Поиск изображения по селекторам
    img_container = soup.select_one('div.single-thumb-container')
    
    img_url = None
    if img_container:
        img_tag = img_container.select_one('img')
        if img_tag:
            # Проверяем наличие атрибутов src, data-src и srcset
            img_url = img_tag.get('data-src')
            print(f"Найденный URL изображения: {img_url}")

    # Поиск заголовка
    title_tag = soup.find('h1', class_='entry-title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        print(title)
    else:
        title = "Заголовок не найден"

    # Функция для удаления стоп-фраз
    def remove_stop_phrases(text, stop_phrases):
        for phrase in stop_phrases:
            index = text.find(phrase)
            if index != -1:
                return text[:index].strip()
        return text

    # Функция для обработки содержимого
    def process_content(soup):
        content_tags = soup.select('div.main-content.article-content')
        if content_tags:
            stop_phrases = [
                "Διαβάστε περισσότερες",
                "Διαβάστε τη συνέχεια στο",
                "Διαβάστε περισσότερα οικονομικά νέα στο",
                "Ειδήσεις σήμερα",
                "Διαβάστε περισσότερα στο",
                "Δείτε την ανάρτησή της",
                "A post shared by"
            ]
            content = ' '.join([remove_stop_phrases(tag.get_text(separator=' ', strip=True), stop_phrases) for tag in content_tags])
            return content
        return "Содержимое не найдено"

    # Обработка содержимого
    content = process_content(soup)

    result = {
        "img_url": img_url,
        "title": title,
        "content": content
    }
    
    formatted_text = f"**{title}**\n\n{tag}"
    send_photo_message_to_telegram(img_url, formatted_text)

    