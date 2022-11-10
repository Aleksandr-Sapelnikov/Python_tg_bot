from loader import bot, BestState, User
import telebot
from config import url_for_city_id, url_for_hotel_list, rapid_api_key, url_for_photo
import requests
import json
import re
from datetime import date, datetime
import time


headers_1 = {
    "content-type": "application/json",
    "X-RapidAPI-Key": rapid_api_key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}
headers = {
    "X-RapidAPI-Key": rapid_api_key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

pattern = r'\b\d{4}\.\d{2}\.\d{2}\b'
pattern_price = r'\b\d{1,4} \d{1,4}\b'
pattern_distance = r'\b\d{1,3}[.]?\d* \d{1,3}[.]?\d*\b'


@bot.message_handler(state=BestState.city)
def best_get_city_id(message):
    user = User.get_user(message.from_user.id)
    user.city = message.text
    user.property_dict.clear()

    bot.send_message(message.chat.id, f"Пробуем найти что-то по городу с названием {user.city}")
    querystring = {"q": user.city.lower(), "locale": "en_US", "langid": "1033", "siteid": "300000001"}

    try:
        response = requests.request("GET", url_for_city_id, headers=headers, params=querystring)
        print(response.text)
        data = json.loads(response.text)
        city_id = data['sr'][0]['gaiaId']
        user.property_dict["regionId"] = city_id
        print(user.property_dict)
        bot.send_message(message.chat.id, "Введите дату заезда (yyyy.mm.dd)")
        bot.set_state(user_id=message.from_user.id, state=BestState.start_date, chat_id=message.chat.id)

    except Exception:
        print('Ошибка в запросе и поиске id города')
        bot.send_message(message.chat.id, "Что-то пошло не так")
        bot.set_state(user_id=message.from_user.id, state=None, chat_id=message.chat.id)


@bot.message_handler(state=BestState.start_date)
def check_in_date(message):
    user = User.get_user(message.from_user.id)
    print(message.text)
    current_date = date.today()
    try:
        if re.fullmatch(pattern, message.text):
            date_list = message.text.split('.')
            current_date_2 = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))

            print(current_date, current_date_2)
            if current_date >= current_date_2:  # дата должна отличатся от текущей
                print('Нельзя выбрать прошедшие дни')
                msg = bot.send_message(message.chat.id, f"Нельзя выбрать прошедшие дни, сейчас: {current_date}"
                                                        f"\nПопробуйте снова")
                bot.register_next_step_handler(msg, check_in_date)

            user.property_dict['checkInDate'] = date_list
            print(user.property_dict)

            bot.send_message(message.chat.id, "Введите дату отъезда (yyyy.mm.dd)")
            bot.set_state(user_id=message.from_user.id, state=BestState.end_date, chat_id=message.chat.id)
        else:
            msg = bot.send_message(message.chat.id, "Нужно вводить как в формате: (yyyy.mm.dd), Попробуй еще.")
            bot.register_next_step_handler(msg, check_in_date)

    except Exception:
        msg = bot.send_message(message.chat.id, "Что-то не срослось, попробуй еще")
        bot.register_next_step_handler(msg, check_in_date)


@bot.message_handler(state=BestState.end_date)
def check_out_date(message):
    user = User.get_user(message.from_user.id)
    print(message.text)
    current_date = date.today()
    try:
        if re.fullmatch(pattern, message.text):
            date_list = message.text.split('.')
            current_date_2 = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
            start_date = date(int(user.property_dict['checkInDate'][0]),
                              int(user.property_dict['checkInDate'][1]),
                              int(user.property_dict['checkInDate'][2]))

            print(current_date, current_date_2, start_date)
            if current_date >= current_date_2 >= start_date:  # дата должна отличатся от текущей и от начальной
                print('Нельзя выбрать прошедшие дни или дни старта')
                msg = bot.send_message(message.chat.id, f"Нельзя выбрать прошедшие дни или день старта,"
                                                        f" сейчас: {current_date}"
                                                        f"\nПопробуйте снова")
                bot.register_next_step_handler(msg, check_out_date)

            user.property_dict['checkOutDate'] = date_list
            print(user.property_dict)

            bot.send_message(message.chat.id, "Введите количество взрослых")
            bot.set_state(user_id=message.from_user.id, state=BestState.adults, chat_id=message.chat.id)
        else:
            msg = bot.send_message(message.chat.id, "Нужно вводить как в формате: (yyyy.mm.dd), Попробуй еще.")
            bot.register_next_step_handler(msg, check_out_date)

    except Exception:
        msg = bot.send_message(message.chat.id, "Что-то не получилось, попробуй еще")
        bot.register_next_step_handler(msg, check_out_date)


@bot.message_handler(state=BestState.adults)
def set_adults(message):
    user = User.get_user(message.from_user.id)
    print(message.text)
    if message.text.isdigit():
        if 1 <= int(message.text) <= 6:
            user.property_dict['adults'] = message.text
            print(user.property_dict)
            bot.send_message(message.chat.id, "Введите диапазон цен через пробел (min max)")
            bot.set_state(user_id=message.from_user.id, state=BestState.price, chat_id=message.chat.id)
        else:
            msg = bot.send_message(message.chat.id, "Попробуйте ввести число от 1 до 6")
            bot.register_next_step_handler(msg, set_adults)
    else:
        msg = bot.send_message(message.chat.id, "Попробуйте ввести число от 1 до 6")
        bot.register_next_step_handler(msg, set_adults)


@bot.message_handler(state=BestState.price)
def set_price(message):
    user = User.get_user(message.from_user.id)
    print(message.text)
    if re.fullmatch(pattern_price, message.text):
        price = message.text.split()
        min_price = int(price[0])
        max_price = int(price[1])
        if max_price > min_price:
            user.property_dict['max_price'] = max_price
            user.property_dict['min_price'] = min_price
            bot.send_message(message.chat.id, "Введите диапазон расстояний от центра (мили) (Пример: 0.1 3 )")
            bot.set_state(user_id=message.from_user.id, state=BestState.destination, chat_id=message.chat.id)

        else:
            msg = bot.send_message(message.chat.id, "Минимальная цена не может быть больше максимальной. "
                                                    "Попробуйте снова")
            bot.register_next_step_handler(msg, set_price)
    else:
        msg = bot.send_message(message.chat.id, "Ввод не соответствует формату (min max), "
                                                "Попробуйте снова")
        bot.register_next_step_handler(msg, set_price)


@bot.message_handler(state=BestState.destination)
def set_destination(message):
    print(message.text)
    user = User.get_user(message.from_user.id)
    if re.fullmatch(pattern_distance, message.text):
        distance = message.text.split()
        try:
            min_dist = float(distance[0])
            max_dist = float(distance[1])
            if max_dist > min_dist:
                user.property_dict['max_dist'] = max_dist
                user.property_dict['min_dist'] = min_dist
                bot.send_message(message.chat.id, "Введите сколько нужно вывести предложений "
                                                  "(Будет меньше из-за сортировки по расстоянию до центра) (max=10)")
                bot.set_state(user_id=message.from_user.id, state=BestState.resultsSize, chat_id=message.chat.id)
        except ValueError:
            msg = bot.send_message(message.chat.id, "При вводе десятичных чисел используйте точку\nПример: 1.11 2.22")
            bot.register_next_step_handler(msg, set_destination)


    else:
        msg = bot.send_message(message.chat.id, "Я Вас не понял, попробуйте еще.\nПример: 1 5\nПример: 1.34 5.12")
        bot.register_next_step_handler(msg, set_destination)


@bot.message_handler(state=BestState.resultsSize)
def get_hotel_list(message):
    user = User.get_user(message.from_user.id)
    print(message.text)
    if message.text.isdigit():
        if 1 <= int(message.text) <= 10:
            user.property_dict['resultsSize'] = message.text
            print(user.property_dict)
        else:
            msg = bot.send_message(message.chat.id, "Попробуйте ввести число от 1 до 10")
            bot.register_next_step_handler(msg, get_hotel_list)
    else:
        msg = bot.send_message(message.chat.id, "Попробуйте ввести число от 1 до 10")
        bot.register_next_step_handler(msg, get_hotel_list)

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": user.property_dict["regionId"]},
        "checkInDate": {
            "day": int(user.property_dict['checkInDate'][2]),
            "month": int(user.property_dict['checkInDate'][1]),
            "year": int(user.property_dict['checkInDate'][0])
        },
        "checkOutDate": {
            "day": int(user.property_dict['checkOutDate'][2]),
            "month": int(user.property_dict['checkOutDate'][1]),
            "year": int(user.property_dict['checkOutDate'][0])
        },
        "rooms": [
            {
                "adults": int(user.property_dict['adults']),
                # "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": int(user.property_dict['resultsSize']),
        "sort": "RECOMMENDED",
        "filters": {"price": {
            "max": user.property_dict['max_price'],
            "min": user.property_dict['min_price']
        }}
    }

    print(payload)
    bot.send_message(message.chat.id, "Обработка...")
    try:
        response = requests.request("POST", url_for_hotel_list, json=payload, headers=headers_1)

        data = json.loads(response.text)

        user.hotel_list.clear()

        for i_hotel in range(int(user.property_dict['resultsSize'])):  # "resultsSize" 10
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
                hotel_price_total = \
                    data['data']['propertySearch']['properties'][i_hotel]['price']['displayMessages'][1]['lineItems'][0]['value']

                current_dict['Id'] = hotel_id
                current_dict['Название отеля'] = hotel_name
                current_dict['Цена за ночь'] = hotel_price_per_night
                current_dict['Всего расходов'] = hotel_price_total
                current_dict['Расстояние от центра (мили)'] = hotel_distance
                current_dict['Превью'] = image_1_link

                image_list = []

                payload_2 = {
                    "currency": "USD",
                    "eapid": 1,
                    "locale": "en_US",
                    "siteId": 300000001,
                    "propertyId": hotel_id
                }
                try:
                    response = requests.request("POST", url_for_photo, json=payload_2, headers=headers)
                    data_2 = json.loads(response.text)
                    try:

                        current_dict['Адрес'] = data_2['data']['propertyInfo'] \
                            ['summary']['location']['address']['addressLine']
                        for img in range(6):  # Максимум фотографий
                            image_list.append(data_2['data']['propertyInfo']
                                              ['propertyGallery']['images'][img]['image']['url'])

                        current_dict['img_links'] = image_list

                    except Exception:
                        print('Ошибка в добавлении фотографий в список')

                except Exception:
                    print('Ошибка в запросе фотографий и адреса')
                    bot.send_message(message.chat.id, "Что-то пошло не так")

                user.hotel_list.append(current_dict)

                print('Текущий словарь', current_dict)
                print('Лист отелей после добавления словаря', user.hotel_list)


            except Exception:
                print('Что-то не так в параметрах отеля')
                bot.send_message(message.chat.id, f"Есть проблемы с некоторыми результатами")

            # user.hotel_list.sort(key=lambda dictionary: float(dictionary['Цена за ночь'][1:]), reverse=True)
            user.hotel_list =\
                list(filter(lambda a: user.property_dict['min_dist']
                            <= a.get('Расстояние от центра (мили)') <= user.property_dict['max_dist'], user.hotel_list))

            print('После сортировки', user.hotel_list)

        print('До запроса фоток', user.hotel_list)

        bot.send_message(message.chat.id, "Нужны фотографии?")
        bot.set_state(user_id=message.from_user.id, state=BestState.photo, chat_id=message.chat.id)

    except Exception:
        print('Ошибка в запросе и поиске hotel list')
        bot.send_message(message.chat.id, "Что-то пошло не так")
        bot.set_state(user_id=message.from_user.id, state=None, chat_id=message.chat.id)


@bot.message_handler(state=BestState.photo)
def set_photo_ans(message):
    user = User.get_user(message.from_user.id)
    print(message.text)
    if message.text.lower() == 'нет' or message.text.lower() == 'no' or message.text.lower() == 'ytn':
        print('После кнопки "нет" ', user.hotel_list)
        for i_elem in range(len(user.hotel_list)):
            my_string = ''
            for i, j in user.hotel_list[i_elem].items():
                if i == 'Id' or i == 'Превью' or i == 'img_links':
                    continue

                else:
                    my_string += f'{i} - {j}\n'

            cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
            user.history[cut_time] = my_string

            bot.send_message(message.chat.id, my_string)
            time.sleep(1)
        bot.set_state(user_id=message.from_user.id, state=None, chat_id=message.chat.id)

    elif message.text.lower() == 'да' or message.text.lower() == 'lf' or message.text.lower() == 'yes':
        print('После кнопки "да" ', user.hotel_list)
        bot.send_message(message.chat.id, "Сколько фотографий нужно? (max = 6)")
        bot.set_state(user_id=message.from_user.id, state=BestState.count_photo, chat_id=message.chat.id)

    else:
        msg = bot.send_message(message.chat.id, "Я тебя не понял, попробуй еще")
        bot.register_next_step_handler(msg, set_photo_ans)


@bot.message_handler(state=BestState.count_photo)
def set_photo(message):
    user = User.get_user(message.from_user.id)
    print(message.text)
    if message.text.isdigit():
        if int(message.text) > 6:
            image_group = []
            print('Выводится максимум фотографий')
            for elem in range(len(user.hotel_list)):
                image_group.clear()
                my_string = ''
                for i, j in user.hotel_list[elem].items():
                    if i == 'Id' or i == 'Превью' or i == 'img_links':
                        continue

                    else:
                        my_string += f'{i} - {j}\n'

                cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
                user.history[cut_time] = my_string

                for num in range(len(user.hotel_list[elem]['img_links'])):
                    image_group.append(
                    telebot.types.InputMediaPhoto(user.hotel_list[elem]['img_links'][num],
                                                  caption=my_string if num == 0 else ''))
                bot.send_media_group(message.chat.id, media=image_group)
                time.sleep(1)

        elif 2 <= int(message.text) <= 6:
            print('Выводится заданное количество фотографий фотографий')
            count = int(message.text)
            image_group = []
            for elem in range(len(user.hotel_list)):
                image_group.clear()
                my_string = ''
                for i, j in user.hotel_list[elem].items():
                    if i == 'Id' or i == 'Превью' or i == 'img_links':
                        continue

                    else:
                        my_string += f'{i} - {j}\n'

                cut_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
                user.history[cut_time] = my_string

                for num in range(count):
                    image_group.append(
                        telebot.types.InputMediaPhoto(user.hotel_list[elem]['img_links'][num],
                                                      caption=my_string if num == 0 else ''))
                bot.send_media_group(message.chat.id, media=image_group)
                time.sleep(1)

        else:
            msg = bot.send_message(message.chat.id, "Количество фотографий от 2 до 6. Попробуйте ввести еще раз")
            bot.register_next_step_handler(msg, set_photo)

    else:
        msg = bot.send_message(message.chat.id, "Что-то не так, убедитесь, что ввели число")
        bot.register_next_step_handler(msg, set_photo)

    bot.set_state(user_id=message.from_user.id, state=None, chat_id=message.chat.id)
