# import requests
# # from project import commands
# from project.config import url_for_city_id, headers
# from project.loader import bot
# import json
# from project.api.hotel_list import check_in_date
# from project.loader import UserState
#
#
# url = url_for_city_id
#
#
# @bot.message_handler(state=UserState.city)
# def get_city_id(message, flag):
#     print("функция get_city_id", message)
#     print(flag)
#     print('состояние', UserState.city)
#     # user_city = message.text
#     # bot.send_message(message.chat.id, f"Привет, пробуем найти что-то по городу с названием {user_city}")
#     # querystring = {"q": user_city.lower(), "locale": "en_US", "langid": "1033", "siteid": "300000001"}
#     # print(querystring['q'])
#     # try:
#     #     response = requests.request("GET", url, headers=headers, params=querystring)
#     #     print(response.text)
#     #     data = json.loads(response.text)
#     #     city_id = data['sr'][0]['gaiaId']
#     #     print(city_id)
#     #     return city_id
#     city_id = '1234'
#     if flag == 'lowprice':
#         print('флаг сработал')
#         bot.set_state(user_id=message.from_user.id, state=UserState.city_id, chat_id=message.chat.id)
#         sent = bot.send_message(message.from_user.id, "Когда заезд?")
#         # bot.register_next_step_handler(message, commands.lowprice.get_properties, city_id)
#         bot.register_next_step_handler(sent, check_in_date, city_id, 'lowprice')  # переходим в hotel_list
#
#     elif flag == 'hightprice':
#         pass
#
#
#     # except Exception:
#     #     print('ошибка')
#     #     bot.send_message(message.from_user.id, "Привет, ничего не найдено")
