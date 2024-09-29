import requests
import json
import logging
# import google.generativeai as genai
# import typing_extensions as typing
from config import GOOGLE_AI_STUDIO_API




# Настройка API ключа

# class ResponseData(typing.TypedDict):
#     title: str
#     content: str

# def send_request_to_google(title, content):
#     model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json", "response_schema":list[ResponseData]})

#     prompt = ["title: " + title + " content: " + content]

#     response = model.generate_content(prompt)
    
#     # Обработка ответа

#     return response  # Возвращаем JSON




  # Ожидается, что это будет JSON с 'title' и 'content'




















def send_request_to_google(title, content):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_AI_STUDIO_API}'
    headers = {'Content-Type': 'application/json'}
    
    # Формирование данных для отправки
    data = {
      "system_instruction": 
            {
                "parts": [
                    {"text": "пост twitter без emoji, размер 360 символов"},
                    # {"text": "В твоем ответе должен быть заголовок, отделенный от основного текста, и в конце hashtag."},
                    {"text":  "Пример желаемого формата Strongly bold with asterisks:  *Это заголовок*\n Основной текст поста. #тег"}
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
    # print(response.json())
    # print("----------------------------------")
    
    # Вывод результата
    # print("Статус код:", response.status_code)
    # print("Ответ:", response.json())


    return response


def extract_text_from_response(response_data):
    try:
        text = response_data['candidates'][0]['content']['parts'][0]['text']
        # print(text)
        text += " #proc"
        return text
    except (KeyError, IndexError) as e:
        logging.error(f"Ошибка при извлечении текста из ответа: {e}")
        return None


