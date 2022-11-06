from api import search_city_id
import loader
from loader import bot, UserState
import commands
import requests
import json
import config

if __name__ == '__main__':
    loader.set_default_commands(loader.bot)
    headers_1 = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.rapid_api_key,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    headers = {
        "X-RapidAPI-Key": config.rapid_api_key,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    # @bot.message_handler(content_types=['text'])
    @bot.message_handler(commands=['lowprice'])
    def start(message):
    # if message.text == '/lowprice':
        sent = bot.send_message(message.from_user.id, "Какой город?")
        print(sent.text)
        bot.set_state(user_id=message.from_user.id, state=UserState.city, chat_id=message.chat.id)

        # bot.register_next_step_handler(sent, search_city_id.get_city_id, 'lowprice')  # переходим в search_city_id с флагом


        # bot.register_next_step_handler(sent, commands.lowprice.low_get_city_id) #>>>> проверял с этой функцией, выполняет и сразу же возвращается, не выполняя следующий шаг, который прописан там

        #bot.register_next_step_handler(sent, low_get_city_id)
        #
        # elif message.text == '/highprice':
        #     pass
        #     # sent = bot.send_message(message.from_user.id, "Какой город?")
        #     # bot.register_next_step_handler(sent, commands.hightprice.get_city_id, 'lowprice')
        # else:
        #     pass


#  +++++++++++++++++++проверка работы в одном файле +++++++++++++++++++++++++++++++++++++ !!Переход работает!!
    # ++++ Варианты с ошибкой ввода пока не рассматриваю ++++
    property_dict = {}
    answer_dict = {}

    @bot.message_handler(state=UserState.city)
    def low_get_city_id(message):
        print("функция get_city_id", message.text)
        answer_dict['Город'] = message.text
        bot.set_state(user_id=message.from_user.id, state=UserState.start_date, chat_id=message.chat.id)
        bot.send_message(message.chat.id, f"Пробуем найти что-то по городу с названием {answer_dict['Город']}")
        querystring = {"q": answer_dict['Город'].lower(), "locale": "en_US", "langid": "1033", "siteid": "300000001"}

        try:
            response = requests.request("GET", config.url_for_city_id, headers=headers, params=querystring)
            print(response.text)
            data = json.loads(response.text)
            city_id = data['sr'][0]['gaiaId']
            property_dict["regionId"] = city_id
        except Exception:
            print('Ошибка в запросе и поиске id города')
            bot.send_message(message.chat.id, "Что-то пошло не так")


        # bot.set_state(user_id=message.from_user.id, state=UserState.city_id, chat_id=message.chat.id)  # эта штука не начто не влияет (не переходит к след. функции)
        # sent = bot.send_message(message.from_user.id, "Когда заезд?")
        # bot.register_next_step_handler(message, commands.lowprice.get_properties, city_id)
        bot.send_message(message.chat.id, "Введите дату заезда (dd.mm.yyyy)")
        bot.set_state(user_id=message.from_user.id, state=UserState.start_date, chat_id=message.chat.id)

    @bot.message_handler(state=UserState.start_date)
    def check_in_date(message):
        print(message.text)
        print('Перешли в чек ин')
        property_dict['checkInDate'] = message.text.split('.')
        print(property_dict)
        bot.send_message(message.chat.id, "Введите дату отъезда (dd.mm.yyyy)")
        bot.set_state(user_id=message.from_user.id, state=UserState.end_date, chat_id=message.chat.id)
        # sent = bot.send_message(message.from_user.id, "Введите дату отъезда (dd.mm.yyyy)")

        # time_list = datetime.strptime(sent.text, '%d %m %Y')

        # bot.register_next_step_handler(sent, check_out_date)
        # sent = bot.send_message(message.from_user.id, "Введите дату заезда (dd.mm.yyyy)")
        #
        # time_list = datetime.strptime(sent.text, '%d.%m.%Y')
        # print(time_list, property_dict)
        # bot.register_next_step_handler(sent, check_out_date)


    # @bot.message_handler(state=UserState.start_date)

    @bot.message_handler(state=UserState.end_date)
    def check_out_date(message):
        print(message.text)

        property_dict['checkOutDate'] = message.text.split('.')
        print(property_dict)
        bot.send_message(message.chat.id, "Введите количество взрослых")
        bot.set_state(user_id=message.from_user.id, state=UserState.adults, chat_id=message.chat.id)


    @bot.message_handler(state=UserState.adults)
    def set_adults(message):
        print(message.text)
        property_dict['adults'] = message.text
        print(property_dict)
        bot.send_message(message.chat.id, "Введите сколько нужно вывести предложений (max=10)")
        bot.set_state(user_id=message.from_user.id, state=UserState.resultsSize, chat_id=message.chat.id)


    # @bot.message_handler(state=UserState.adults)
    # def set_adults(message):
    #     print(message.text)
    #     property_dict['resultsSize'] = message.text
    #     print(property_dict)
    #     bot.send_message(message.chat.id, "Введите количество взрослых")
    #     bot.set_state(user_id=message.from_user.id, state=UserState.answer, chat_id=message.chat.id)

    @bot.message_handler(state=UserState.resultsSize)
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
                "sort": "PRICE_LOW_TO_HIGH",
                "filters": {"price": {
                        "max": 200,
                        "min": 30
                    }}
            }

        print(payload)
        bot.send_message(message.chat.id, "Обработка...")
        try:
            response = requests.request("POST", config.url_for_hotel_list, json=payload, headers=headers_1)
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
                    hotel_price_per_night = data['data']['propertySearch']['properties'][i_hotel]['price']['strikeOut'][
                        'formatted']
                    hotel_distance = \
                    data['data']['propertySearch']['properties'][i_hotel]['destinationInfo']['distanceFromDestination']['value']
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
                    my_string += f'{i} - {j}\n'

                bot.send_message(message.chat.id, my_string)
            # bot.send_message(message.chat.id, f"Результат:\n{hotel_list}")

        except Exception:
            print('Ошибка в запросе и поиске hotel list')
            bot.send_message(message.chat.id, "Что-то пошло не так")
        # response = requests.request("POST", config.url_for_hotel_list, json=payload, headers=headers_1)


        # data = json.loads(response.text)
        # hotel_list = []
        # for i_hotel in range(int(property_dict['resultsSize'])):  # "resultsSize" 10
        #     current_dict = {}
        #     hotel_id = data['propertySearch']['properties'][str(i_hotel)]['id']
        #     hotel_name = data['propertySearch']['properties'][str(i_hotel)]['name']
        #     hotel_price_per_night = data['propertySearch']['properties'][str(i_hotel)]['price']['strikeOut']['formatted']
        #     hotel_distance = data['propertySearch']['properties'][str(i_hotel)]['destinationInfo']['distanceFromDestination']['value']
        #     current_dict['Id'] = hotel_id
        #     current_dict['name'] = hotel_name
        #     current_dict['price'] = hotel_price_per_night
        #     current_dict['distance(mil)'] = hotel_distance
        #     hotel_list.append(current_dict)
        # print(hotel_list)
        # bot.send_message(message.chat.id, f"Результат:\nГород:{answer_dict['Город']}\nОтель:{current_dict['name']}")
        # bot.send_message(message.chat.id, f"Результат:\n{hotel_list}")


    loader.bot.infinity_polling()