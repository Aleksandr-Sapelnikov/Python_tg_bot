rapid_api_key = "your api key"
bot_token = 'your bot token'
url_for_city_id = "https://hotels4.p.rapidapi.com/locations/v3/search"
url_for_hotel_list = "https://hotels4.p.rapidapi.com/properties/v2/list"
url_for_photo = "https://hotels4.p.rapidapi.com/properties/v2/get-summary"
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
