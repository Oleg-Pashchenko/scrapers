from __future__ import annotations

import datetime
import time
import lxml
import requests
import bs4

from db.source import SourceScraper
from misc.models import SourceItem, SecretInfo


def scrape(item_code: int) -> SourceItem | None:
    try:
        link = f"https://www.oreht.ru/modules.php?name=orehtPriceLS&op=ShowInfo&code={item_code}"
        r = requests.get(link)
        soup = bs4.BeautifulSoup(r.text, features="lxml")
        name = soup.find("div", {"class": "mg-h1text"}).text
        img = soup.find("div", {"class": "mg-glimage"}).find("img").get("src")
        price = soup.find("div", {"class": "mg-price"})

        name = name.strip()
        img = "https://www.oreht.ru/" + img.strip()
        price = float(
            price.find("span", "mg-price-n").text.strip()
            + "."
            + price.find_all("span", "mg-price-n")[1].text.strip()
        )
        return SourceItem(
            name=name,
            link=link,
            photo=img,
            id=item_code,
            price=price,
            creation_date=datetime.datetime.now(),
        )
    except Exception as e:
        print(e)
        return None


def oreht_scraper():
    source_db = SourceScraper(table_name="oreht_positions")
    while True:
        try:
            code, date = source_db.get_code()
            if not code:
                time.sleep(5)
                continue
            item = scrape(code)
            now = datetime.datetime.now()
            if not item:
                source_db.save_to_error_db("oreht_errors", code, date, now)
            source_db.save_to_mk("ozon", item)
            source_db.save_to_mk("wilberries", item)
        except:
            pass