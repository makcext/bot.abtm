from ast import Await
from time import sleep
import requests
from bs4 import BeautifulSoup
import requests
import json
from gemini import send_request_to_google, extract_text_from_response
from notify import send_photo_message_to_telegram


import logging





def parser_protothema(url, tag):
    
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  print("parser protothema")

    # Поиск изображения по селекторам
  img_container = soup.select_one('body > div.outer > main > section.section.mainSection > div > div.articleContainer > div.articleContainer__media > div.imgWrp > div > div > div')
  
  img_url = None
  if img_container:
      img_tag = img_container.select_one('picture img')
      if img_tag and 'src' in img_tag.attrs:
          img_url = img_tag['src']
          print("img_url", img_url)

  else:
    img_url = "kfkf.jpg"


  title_tag = soup.find('div', class_='title title--noDot')
  if title_tag:
      title = title_tag.get_text()
  else:
      title = "Заголовок не найден"



  def remove_stop_phrases(text, stop_phrases):
      for phrase in stop_phrases:
          index = text.find(phrase)
          if index != -1:
              return text[:index].strip()
      return text

  def process_content(soup):
    content_tags = soup.select('body > div.outer > main > section.section.mainSection > div > div.articleContainer > div.articleContainer__main > div.cnt')
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

  # В функции perser_protothema:
  content = process_content(soup)
  print("content", content)


  # print(img_url, title, content)

  result = {
        "img_url": img_url,
        "title": title,
        "content": content
    }
  data = result
    
  ai_message = send_request_to_google(data['title'], data['content'])
  extracted_text = extract_text_from_response(ai_message.json())
  send_photo_message_to_telegram(data['img_url'], extracted_text)

  return result

# url = "https://www.protothema.gr/world/article/1545686/nekros-kai-o-anaplirotis-dioikitis-ton-frouron-tis-epanastasis-apo-israilina-pligmata-anamenetai-skliri-iraniki-apadisi/"
# tag = "#tag1"
# result = parser_protothema(url, tag)

# url = "https://www.protothema.gr/life-style/article/1541045/seferlis-enadion-parousiaston-psuhagogikon-ekpobon-tha-tous-xebrostiaso-olous-me-epiheirimata-tha-perasoume-oraia/"
# data = (perser_protothema(url))
# print(data)
# print("----------------------------------")
# ai_message = send_request_to_google(data['title'], data['content'])
# print(ai_message)


#test
# url = "https://www.protothema.gr/politics/article/1541220/notopoulou-dehomai-hudaies-epitheseis-apo-opadous-tou-kasselaki-na-min-kruftei-piso-apo-upokritikes-katadikes/"

# data = (perser_protothema(url))
# ai_message = send_request_to_google(data['title'], data['content'])
# extracted_text = extract_text_from_response(ai_message.json())
# send_photo_message_to_telegram(data['img_url'], extracted_text)
# sleep(1.7)


# url = "https://www.protothema.gr/economy/article/1541055/pikros-o-kafes-arabica-rekor-13-eton-ekanan-oi-times-auxithikan-40-to-2024/"
# data = (perser_protothema(url))
# ai_message = send_request_to_google(data['title'], data['content'])
# extracted_text = extract_text_from_response(ai_message.json())
# send_photo_message_to_telegram(data['img_url'], extracted_text)
# sleep(1.8)

# url = "https://www.protothema.gr/life-style/article/1541045/seferlis-enadion-parousiaston-psuhagogikon-ekpobon-tha-tous-xebrostiaso-olous-me-epiheirimata-tha-perasoume-oraia/"
# data = (perser_protothema(url))
# ai_message = send_request_to_google(data['title'], data['content'])
# extracted_text = extract_text_from_response(ai_message.json())
# if extracted_text is not None:
#     send_photo_message_to_telegram(data['img_url'], extracted_text)
# sleep(1.9)
# url = "https://www.protothema.gr/economy/article/1541129/kratikos-proupologismos-pleonasma-148-dis-euro-tin-periodo-ianouariou-augoustou-2024/"
# data = (perser_protothema(url))
# ai_message = send_request_to_google(data['title'], data['content'])
# extracted_text = extract_text_from_response(ai_message.json())
# send_photo_message_to_telegram(data['img_url'], extracted_text)
# sleep(2)







