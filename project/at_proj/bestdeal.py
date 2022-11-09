from loader import bot, BestState
from config import url_for_city_id, url_for_hotel_list, rapid_api_key
import requests
import json

property_dict = {}
answer_dict = {}
headers_1 = {
    "content-type": "application/json",
    "X-RapidAPI-Key": rapid_api_key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}
headers = {
    "X-RapidAPI-Key": rapid_api_key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


@bot.message_handler(state=BestState.city)
def low_get_city_id(message):
    print("функция low_get_city_id", message.text)
    answer_dict['Город'] = message.text
    bot.set_state(user_id=message.from_user.id, state=BestState.start_date, chat_id=message.chat.id)
    bot.send_message(message.chat.id, f"Пробуем найти что-то по городу с названием {answer_dict['Город']}")
    querystring = {"q": answer_dict['Город'].lower(), "locale": "en_US", "langid": "1033", "siteid": "300000001"}

    try:
        response = requests.request("GET", url_for_city_id, headers=headers, params=querystring)
        print(response.text)
        data = json.loads(response.text)
        city_id = data['sr'][0]['gaiaId']
        property_dict["regionId"] = city_id
    except Exception:
        print('Ошибка в запросе и поиске id города')
        bot.send_message(message.chat.id, "Что-то пошло не так")

    bot.send_message(message.chat.id, "Введите дату заезда (dd.mm.yyyy)")
    bot.set_state(user_id=message.from_user.id, state=BestState.start_date, chat_id=message.chat.id)


@bot.message_handler(state=BestState.start_date)
def check_in_date(message):
    print(message.text)
    print('Перешли в чек ин')
    property_dict['checkInDate'] = message.text.split('.')
    print(property_dict)
    bot.send_message(message.chat.id, "Введите дату отъезда (dd.mm.yyyy)")
    bot.set_state(user_id=message.from_user.id, state=BestState.end_date, chat_id=message.chat.id)


@bot.message_handler(state=BestState.end_date)
def check_out_date(message):
    print(message.text)

    property_dict['checkOutDate'] = message.text.split('.')
    print(property_dict)
    bot.send_message(message.chat.id, "Введите количество взрослых")
    bot.set_state(user_id=message.from_user.id, state=BestState.adults, chat_id=message.chat.id)


@bot.message_handler(state=BestState.adults)
def set_adults(message):
    print(message.text)
    property_dict['adults'] = message.text
    print(property_dict)
    bot.send_message(message.chat.id, "Введите диапазон цен через пробел (min max)")
    bot.set_state(user_id=message.from_user.id, state=BestState.price, chat_id=message.chat.id)


# @bot.message_handler(state=BestState.price)
# def set_adults(message):
#     print(message.text)
#     property_dict['price'] = message.text.split()
#     print(property_dict)
#     bot.send_message(message.chat.id, "Введите диапазон расстояний от центра")
#     bot.set_state(user_id=message.from_user.id, state=BestState.destination, chat_id=message.chat.id)


@bot.message_handler(state=BestState.price)
def set_adults(message):
    print(message.text)
    property_dict['adults'] = message.text.split()
    print(property_dict)
    bot.send_message(message.chat.id, "Введите сколько нужно вывести предложений (max=10)")
    bot.set_state(user_id=message.from_user.id, state=BestState.resultsSize, chat_id=message.chat.id)


@bot.message_handler(state=BestState.resultsSize)
def get_hotel_list(message):
    print(message.text)
    property_dict['resultsSize'] = message.text
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": property_dict["regionId"]},
        "checkInDate": {
            "day": int(property_dict['checkInDate'][0]),
            "month": int(property_dict['checkInDate'][1]),
            "year": int(property_dict['checkInDate'][2])
        },
        "checkOutDate": {
            "day": int(property_dict['checkOutDate'][0]),
            "month": int(property_dict['checkOutDate'][1]),
            "year": int(property_dict['checkOutDate'][2])
        },
        "rooms": [
            {
                "adults": int(property_dict['adults']),
                # "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": int(property_dict['resultsSize']),
        "sort": "RECOMMENDED",
        "filters": {"price": {
            "max": int(property_dict['adults'][1]),
            "min": int(property_dict['adults'][0])
        }}
    }

    print(payload)
    bot.send_message(message.chat.id, "Обработка...")
    try:
        response = requests.request("POST", url_for_hotel_list, json=payload, headers=headers_1)
        # print(response.text)
        data = json.loads(response.text)

        #  для проверки
        with open('my_test.json', 'w') as file:
            json.dump(data, file, indent=4)

        hotel_list = []

        for i_hotel in range(int(property_dict['resultsSize'])):  # "resultsSize" 10
            try:
                current_dict = {}
                hotel_id = data['data']['propertySearch']['properties'][i_hotel]["id"]
                hotel_name = data['data']['propertySearch']['properties'][i_hotel]['name']
                hotel_price_per_night = data['data']['propertySearch']['properties'][i_hotel]['price']['lead'][
                    'formatted']
                hotel_distance = \
                    data['data']['propertySearch']['properties'][i_hotel]['destinationInfo']['distanceFromDestination'][
                        'value']
                image_1_link = data['data']['propertySearch']['properties'][i_hotel]['propertyImage']['image']['url']
                current_dict['Id'] = hotel_id
                current_dict['Название отеля'] = hotel_name
                current_dict['Цена за ночь'] = hotel_price_per_night
                current_dict['Расстояние от центра (мили)'] = hotel_distance
                current_dict['Превью'] = image_1_link

                hotel_list.append(current_dict)
                print(current_dict)
            except Exception:
                print('Что-то не так в параметрах отеля')
                bot.send_message(message.chat.id, f"Есть проблемы с некоторыми результатами")

        print(hotel_list)

        for i_elem in range(len(hotel_list)):
            my_string = ''
            for i, j in hotel_list[i_elem].items():
                if i == 'Id':
                    continue
                elif i == 'Превью':
                    image = j
                else:
                    my_string += f'{i} - {j}\n'
            bot.send_photo(message.chat.id, image, my_string)

    except Exception:
        print('Ошибка в запросе и поиске hotel list')
        bot.send_message(message.chat.id, "Что-то пошло не так")
    finally:
        bot.set_state(user_id=message.from_user.id, state=None, chat_id=message.chat.id)
