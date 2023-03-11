import datetime
import random

import psycopg2

from misc.models import SourceItem, MarketPlaceItem
from misc.secrets import secret_info
from scrapers.item_loads import load_ozon


class PresentationScraper:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=secret_info.POSTGRES_HOST,
            database=secret_info.POSTGRES_DBNAME,
            user=secret_info.POSTGRES_USER,
            password=secret_info.POSTGRES_PASSWORD,
        )
        self.cur = self.conn.cursor()

    def get_item(self):
        self.cur.execute("SELECT * FROM presentation;")
        records = self.cur.fetchall()
        record = random.choice(records)
        if record:
            # self.delete_item(record[0])
            si = SourceItem(
                id=record[5],
                link=record[6],
                photo=record[7],
                name=record[8],
                price=record[9],
                creation_date=record[10],
            )
            return MarketPlaceItem(
                id=record[0],
                link=record[1],
                photo=record[2],
                name=record[3],
                price=record[4],
                source_item=si,
            )

    def delete_item(self, id):
        self.cur.execute(f"DELETE FROM presentation WHERE id = %s", (id,))
        self.conn.commit()

    def write_result(self, id):
        self.cur.execute("SELECT * FROM presentation WHERE id = %s;", (id,))
        record = self.cur.fetchone()
        si = SourceItem(
                id=record[5],
                link=record[6],
                photo=record[7],
                name=record[8],
                price=record[9],
                creation_date=record[10],
            )
        item = MarketPlaceItem(
                id=record[0],
                link=record[1],
                photo=record[2],
                name=record[3],
                price=record[4],
                source_item=si,
            )
        load_ozon(item)
        self.cur.execute(
            f"""INSERT INTO result (id, link, photo, name, 
                        price, source_id, source_link, source_photo, source_name, source_price, source_creation_date)
                                 SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM result WHERE id=%s)""",
            (
                record[0],
                record[1],
                record[2],
                record[3],
                record[4],
                record[5],
                record[6],
                record[7],
                record[8],
                record[9],
                record[10],
                record[0],
            ),
        )
        self.conn.commit()

    def write_error(self, id):
        self.cur.execute("SELECT * FROM presentation WHERE id = %s;", (id,))
        record = self.cur.fetchone()
        self.cur.execute(
            f"""INSERT INTO presentation_error (id, link, photo, name, 
                        price, source_id, source_link, source_photo, source_name, source_price, source_creation_date, check_date)
                                 SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM result_error WHERE id=%s)""",
            (
                record[0],
                record[1],
                record[2],
                record[3],
                record[4],
                record[5],
                record[6],
                record[7],
                record[8],
                record[9],
                record[10],
                datetime.datetime.now(),
                record[0],
            ),
        )
