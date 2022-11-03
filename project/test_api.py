import requests
import json

url = "https://hotels4.p.rapidapi.com/properties/v2/list"

payload = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": {"regionId": "2114"},  # делал запрос на Лондон ("https://hotels4.p.rapidapi.com/locations/v3/search")
    "checkInDate": {
        "day": 16,
        "month": 11,
        "year": 2022
    },
    "checkOutDate": {
        "day": 17,
        "month": 11,
        "year": 2022
    },
    "rooms": [
        {
            "adults": 2,
            # "children": [{"age": 5}, {"age": 7}]
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 10,
    "sort": "PRICE_LOW_TO_HIGH",
    "filters": {"price": {
            "max": 500,
            "min": 10
        }}
}
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "962b98a548msh1dd81b569a78ec7p1538eejsn873316f46a92",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)

data = json.loads(response.text)

with open('my_test.json', 'w') as file:
    json.dump(data, file, indent=4)
