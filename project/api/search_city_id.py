import requests
from project.config import url_for_city_id, headers
from project.loader import bot
import json
from project import commands


url = url_for_city_id


def get_city_id(message):  # удивительно, но это работает
    print("функция get_city_id")
    user_city = message.text
    bot.send_message(message.chat.id, f"Привет, пробуем найти что-то по городу с названием {user_city}")
    querystring = {"q": user_city.lower(), "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    print(querystring['q'])
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
        data = json.loads(response.text)
        city_id = data['sr'][0]['gaiaId']
        print(city_id)
        return city_id

    except Exception:
        print('ошибка')
        bot.send_message(message.from_user.id, "Привет, ничего не найдено")
