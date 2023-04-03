import time

import requests
import json

from misc.models import SourceItem, MarketPlaceItem

client_id = '855070'
api_key = 'd18cee5b-aa0a-4723-b57f-ed05ce26a2a3'
headers = {
    'Client-Id': client_id,
    'Api-Key': api_key
}

def load_item(item):
    url = 'https://api-seller.ozon.ru/v1/product/import-by-sku'
    data = {
        "items": [
            {
                "sku": item.id,
                "name": "test from code20",
                "offer_id": item.name,
                "currency_code": "RUB",
                "old_price": "2590",
                "price": "2300",
                "premium_price": "2200",
                "vat": "0.1"
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()
    return response['result']['task_id']


def upload_status(task_id):
    url = 'https://api-seller.ozon.ru/v1/product/import/info'
    data = {'task_id': task_id}
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()
    return not len(response['result']['items'][0]['errors']) > 0, response['result']['items'][0]['product_id'],\
        response['result']['items'][0]['offer_id']

def to_archive(product_id):
    url = 'https://api-seller.ozon.ru/v1/product/archive'
    data = {'product_id': [product_id]}
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()
    print(response)


def to_delete(offer_id):
    url = 'https://api-seller.ozon.ru/v2/products/delete'
    data = {'products': [{'offer_id': offer_id}]}
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()
    print(response)

def has_not_block(mk_item: MarketPlaceItem) -> bool:
    task_id = load_item(mk_item)
    status, product_id, offer_id = upload_status(task_id)
    return status

