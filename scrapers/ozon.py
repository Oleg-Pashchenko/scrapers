import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from db.marketplace import MarketPlaceScraper
from misc.models import SourceItem, MarketPlaceItem
from bs4 import BeautifulSoup
from misc.secrets import secret_info


def scrape(source_item: SourceItem) -> list[MarketPlaceItem]:
    try:
    #if True:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        if secret_info.IS_SERVER == "+":
            driver = webdriver.Chrome(
                executable_path="/usr/bin/chromedriver", chrome_options=chrome_options
            )
        else:
            driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(
            f"https://www.ozon.ru/search/?text={source_item.name}&from_global=true"
        )
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        driver.quit()
        items = (
            soup.find("div", {"class": "widget-search-result-container"})
            .find("div")
            .find_all("div")
        )
        ozon_items = []
        for item in items:
            try:
            #if True:
                description_block = str(item)
                try:
                    price = description_block.split("₽")[0].split(">")[-1]
                    price = float(
                        "".join(price.replace("thinsp;", "").replace(",", ".").split())
                    )
                except:
                    continue
                descr = (
                    description_block.split("</span></span></a>")[0]
                    .split("<span>")[-1]
                    .strip()
                )
                ozon_item_link_el = item.findNext("a")
                if not ozon_item_link_el:
                    continue
                ozon_item_link = "https://www.ozon.ru" + ozon_item_link_el.get("href")
                ozon_id = ozon_item_link.split("/?")[0].split("-")[-1]
                if ozon_id == 'https://www.ozon.ruhttps://job.ozon.ru/' or ozon_item_link_el.find("img") is None:
                    continue
                img = ozon_item_link_el.find("img").get("src")
                ozon_items.append(
                    MarketPlaceItem(
                        id=int(ozon_id),
                        link=ozon_item_link,
                        name=descr,
                        photo=img,
                        source_item=source_item,
                        price=price,
                    )
                )
            except Exception as e:
                print("Ozon:", e)
                pass
        driver.quit()
    except Exception as e:
        print("Ozon:", e)
        ozon_items = []
    return ozon_items


def ozon_scraper():
    source_db = MarketPlaceScraper(table_name="ozon")
    while True:
        source_item = source_db.get_source_item()
        if not source_item:
            time.sleep(5)
            continue
        items = scrape(source_item)
        now = datetime.datetime.now()
        if not items:
            source_db.save_to_error_mk("ozon_error", source_item, now)
        for item in items:
            source_db.save_to_neural("neural", item)
