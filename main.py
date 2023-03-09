import threading
from scrapers.ozon import ozon_scraper
from scrapers.oreht import oreht_scraper
from scrapers.wilberries import wilberries_scraper
from views.tg_bot import tg_bot
from views.site import site
from scrapers.neural_block import neural_block_scraper
from db import db_initialization


def app():
    db_initialization.initialize()
    oreht_thread = threading.Thread(target=oreht_scraper)
    ozon_thread = threading.Thread(target=ozon_scraper)
    wilberries_thread = threading.Thread(target=wilberries_scraper)
    neural_block_thread = threading.Thread(target=neural_block_scraper)
    telegram_bot_thread = threading.Thread(target=tg_bot)
    site_thread = threading.Thread(target=site)
    threads = [
        oreht_thread,
        ozon_thread,
        wilberries_thread,
        neural_block_thread,
        telegram_bot_thread,
        site_thread,
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]


if __name__ == "__main__":
    app()
