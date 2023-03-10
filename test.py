import requests
import json


def load_item():
    client_id = '855070'
    api_key = 'd1fde5e2-2bd2-4aa8-9e11-6c19de58e278'
    headers = {
        'Client-Id': client_id,
        'Api-Key': api_key
    }
    url = 'https://api-seller.ozon.ru/v1/product/import-by-sku'
    data = {
        "items": [
            {
                "sku": 298789742,
                "name": "test from code",
                "offer_id": "91132",
                "currency_code": "RUB",
                "old_price": "2590",
                "price": "2300",
                "premium_price": "2200",
                "vat": "0.1"
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
