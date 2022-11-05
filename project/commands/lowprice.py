from project.loader import bot
import requests
import json
# from project.api.search_city_id import get_city_id
from project.config import url_for_city_id, headers, url_for_hotel_list
from project.loader import UserState
from datetime import datetime

url = url_for_city_id
property_dict = {}
answer_dict = {}


@bot.message_handler(state=UserState.city)
# @bot.message_handler(content_types=['text'])
def low_get_city_id(message):
    print("функция get_city_id", message.text)
    answer_dict['Город'] = message.text
    print('состояние', UserState.city)
    # user_city = message.text
    # bot.send_message(message.chat.id, f"Привет, пробуем найти что-то по городу с названием {user_city}")
    # querystring = {"q": user_city.lower(), "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    # print(querystring['q'])
    # try:
    #     response = requests.request("GET", url, headers=headers, params=querystring)
    #     print(response.text)
    #     data = json.loads(response.text)
    #     city_id = data['sr'][0]['gaiaId']
    #     print(city_id)
    #     return city_id
    city_id = '1234'
    property_dict["regionId"] = city_id
    #bot.set_state(user_id=message.from_user.id, state=UserState.city_id, chat_id=message.chat.id)  # эта штука не начто не влияет (не переходит к след. функции)
    # sent = bot.send_message(message.from_user.id, "Когда заезд?")
    # bot.register_next_step_handler(message, commands.lowprice.get_properties, city_id)

    sent = bot.send_message(message.chat.id, "Введите дату заезда (dd.mm.yyyy)")
    bot.set_state(user_id=message.from_user.id, state=UserState.start_date, chat_id=message.chat.id)

    bot.register_next_step_handler(sent, check_in_date)  # этот шаг уже не работает


@bot.message_handler(state=UserState.start_date)
def check_in_date(message):
    print(message.text)
    print('Перешли в чек ин')
    property_dict['checkInDate'] = message.text.split('.')
    print(property_dict)
    # sent = bot.send_message(message.from_user.id, "Введите дату отъезда (dd.mm.yyyy)")

    # time_list = datetime.strptime(sent.text, '%d %m %Y')

    # bot.register_next_step_handler(sent, check_out_date)
    # sent = bot.send_message(message.from_user.id, "Введите дату заезда (dd.mm.yyyy)")
    #
    # time_list = datetime.strptime(sent.text, '%d.%m.%Y')
    # print(time_list, property_dict)
    # bot.register_next_step_handler(sent, check_out_date)

@bot.message_handler(state=UserState.end_date)
# @bot.message_handler(content_types=['text'])
def check_out_date(message):

    print('Перешли в чек аут')
    property_dict['checkOutDate'] = message.text.split('.')
    print(property_dict)

    # тут запрос если есть ответ "<Response [200]>", то получаем id и продолжаем запрашивать данные,
    # если нет, то ошибка

# if __name__ == '__main__':
#     bot.infinity_polling()