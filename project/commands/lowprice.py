from project.loader import bot
import requests
import json
from project.api.hotel_list import get_hotel_list
from project.config import url_for_city_id, headers

url = url_for_city_id

def get_lowprice(message):
    pass
def get_properties(city_id):
    get_hotel_list(city_id)



    # тут запрос если есть ответ "<Response [200]>", то получаем id и продолжаем запрашивать данные,
    # если нет, то ошибка

