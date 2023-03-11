import datetime

import time

import requests

from db.marketplace import MarketPlaceScraper
from misc.models import MarketPlaceItem, SourceItem


def scrape(source_item: SourceItem):
    result = []
    try:
        url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,7,3,6,5,18,21&curr=rub&dest=-1216601,-337422,-1114902,-1198055&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query={source_item.name}&reg=0&regions=80,64,83,4,38,33,70,68,69,86,30,40,48,1,66,31,22&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false"
        r = requests.get(url).json()
        for i in r["data"]["products"][:10]:
            try:
                if len(str(i["id"])) == 9:
                    vol = str(i["id"])[:4]
                else:
                    vol = str(i["id"])[:3]
                for j in range(1, 11):
                    if j < 10:
                        basket = f"0{j}"
                    else:
                        basket = j
                    photo_url = f'https://basket-{basket}.wb.ru/vol{vol}/part{str(i["id"])[:-3]}/{i["id"]}/images/c516x688/1.jpg'
                    res = requests.get(photo_url)
                    if res.status_code == 200:
                        result.append(
                            MarketPlaceItem(
                                id=i["id"],
                                link=f'https://www.wildberries.ru/catalog/{i["id"]}/detail.aspx',
                                photo=photo_url,
                                name=i["name"],
                                price=int(i["salePriceU"]) / 100,
                                source_item=source_item,
                            )
                        )
                        break
            except Exception as e:
                print("Wilberries:", e)
                pass
    except Exception as e:
        print("Wilberries:", e)
        return []
    return result


def wilberries_scraper():
    source_db = MarketPlaceScraper(table_name="wilberries")
    while True:
        try:
            source_item = source_db.get_source_item()
            if not source_item:
                time.sleep(5)
                continue
            items = scrape(source_item)
            now = datetime.datetime.now()
            if not items:
                source_db.save_to_error_mk("wilberries_error", source_item, now)
            for item in items:
                source_db.save_to_neural("neural", item)
        except:
            pass
