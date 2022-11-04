
bot_token = '5758636146:AAG6tkWwx1to2aNPEAZQVDIav1W-mGhJyWA'

rapid_api_key = "962b98a548msh1dd81b569a78ec7p1538eejsn873316f46a92"

url_for_city_id = "https://hotels4.p.rapidapi.com/locations/v3/search"

url_for_hotel_list = "https://hotels4.p.rapidapi.com/properties/v2/list"

headers = {
    "X-RapidAPI-Key": rapid_api_key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', 'Поиск бюджетных отелей'),
    ('highprice', 'Поиск лучших отелей'),
    ('bestdeal', 'Настройка поиска'),
    ('history', 'История поиска')
)