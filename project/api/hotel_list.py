# import requests
# import json
# from project.config import url_for_hotel_list, rapid_api_key
# from project.loader import bot
# from datetime import datetime
# from project.loader import UserState
# url = url_for_hotel_list
#
# property_list = []
# property_dict = {}
# # command_flag = None
#
#
# @bot.message_handler(state=UserState.city_id)
# def check_in_date(message, city_id, flag):
#     command_flag = flag
#     property_dict["regionId"] = city_id
#     sent = bot.send_message(message.from_user.id, "Введите дату заезда (dd.mm.yyyy)")
#
#     time_list = datetime.strptime(sent.text, '%d.%m.%Y')
#     print(time_list, property_dict, command_flag)
#     # bot.register_next_step_handler(sent, check_out_date)
#
#
# @bot.message_handler(state=UserState.start_date)
# def check_out_date(message):
#     print('Задаем дату отъезда')
#
#     # sent = bot.send_message(message.from_user.id, "Введите дату возвращения (dd.mm.yy)")
#     # bot.register_next_step_handler(sent, search_city_id.get_city_id)
#
#
# def get_hotel_list(city_id):  # Сюда как-то надо передать city_id
#     payload = {
#         "currency": "USD",
#         "eapid": 1,
#         "locale": "en_US",
#         "siteId": 300000001,
#         "destination": {"regionId": city_id},
#         "checkInDate": {
#             "day": 10,
#             "month": 12,
#             "year": 2022
#         },
#         "checkOutDate": {
#             "day": 15,
#             "month": 12,
#             "year": 2022
#         },
#         "rooms": [
#             {
#                 "adults": 2,
#                 # "children": [{"age": 5}, {"age": 7}]
#             }
#         ],
#         "resultsStartingIndex": 0,
#         "resultsSize": 10,
#         "sort": "PRICE_LOW_TO_HIGH",
#         "filters": {"price": {
#                 "max": 200,
#                 "min": 30
#             }}
#     }
#     headers = {
#         "content-type": "application/json",
#         "X-RapidAPI-Key": rapid_api_key,
#         "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
#     }
#
#     response = requests.request("POST", url, json=payload, headers=headers)
#
#     print(response.text)
#     data = json.loads(response.text)
#     hotel_list = []
#     for i_hotel in range(10):  # "resultsSize" 10
#         current_dict = {}
#         hotel_id = data['propertySearch']['properties'][str(i_hotel)]['id']
#         hotel_name = data['propertySearch']['properties'][str(i_hotel)]['name']
#         hotel_price_per_night = data['propertySearch']['properties'][str(i_hotel)]['price']['strikeOut']['formatted']
#         hotel_distance = data['propertySearch']['properties'][str(i_hotel)]['destinationInfo']['distanceFromDestination']['value']
#         current_dict['Id'] = hotel_id
#         current_dict['name'] = hotel_name
#         current_dict['price'] = hotel_price_per_night
#         current_dict['distance(mil)'] = hotel_distance
#         hotel_list.append(current_dict)
#
#     print(hotel_list)