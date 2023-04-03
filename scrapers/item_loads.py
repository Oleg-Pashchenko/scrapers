import requests
import json

from misc.models import MarketPlaceItem, SourceItem


def load_ozon(item: MarketPlaceItem):
    client_id = '667260'
    api_key = 'fd6087c6-de11-43ee-a233-4540cb92998a'
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
                "offer_id": "РСВ-" + str(item.source_item.id) + "РСВ-" + str(item.source_item.id),
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

