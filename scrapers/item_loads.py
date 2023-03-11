import requests
import json

from misc.models import MarketPlaceItem


def load_item(item: MarketPlaceItem):
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
                "sku": str(item.id),
                "name": item.name,
                "offer_id": str(item.source_item.id),
                "currency_code": "RUB",
                "old_price": "10000",
                "price": "10000",
                "premium_price": "10000",
                "vat": "0"
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
