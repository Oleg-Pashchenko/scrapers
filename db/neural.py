from datetime import datetime

import psycopg2

from misc.models import SourceItem, MarketPlaceItem
from misc.secrets import secret_info


class NeuralScraper:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=secret_info.POSTGRES_HOST,
            database=secret_info.POSTGRES_DBNAME,
            user=secret_info.POSTGRES_USER,
            password=secret_info.POSTGRES_PASSWORD,
        )
        self.cur = self.conn.cursor()

    def get_item(self):
        self.cur.execute("SELECT * FROM neural;")
        record = self.cur.fetchone()
        if record:
            self.delete_item(record[0])
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
        self.cur.execute(f"DELETE FROM neural WHERE id = %s", (id,))
        self.conn.commit()

    def write_error(self, mk_item):
        data = mk_item.source_item
        self.cur.execute(
            f"""INSERT INTO neural_error (id, link, photo, name, 
                        price, source_id, source_link, source_photo, source_name, source_price, source_creation_date, check_date)
                                 SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM neural_error WHERE id=%s)""",
            (
                mk_item.id,
                mk_item.link,
                mk_item.photo,
                mk_item.name,
                mk_item.price,
                data.id,
                data.link,
                data.photo,
                data.name,
                data.price,
                data.creation_date,
                datetime.now(),
                mk_item.id,
            ),
        )
        self.conn.commit()

    def write_presentation(self, mk_item):
        data = mk_item.source_item
        self.cur.execute(
            f"""INSERT INTO presentation (id, link, photo, name, 
                price, source_id, source_link, source_photo, source_name, source_price, source_creation_date)
                         SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM presentation WHERE id=%s)""",
            (
                mk_item.id,
                mk_item.link,
                mk_item.photo,
                mk_item.name,
                mk_item.price,
                data.id,
                data.link,
                data.photo,
                data.name,
                data.price,
                data.creation_date,
                mk_item.id,
            ),
        )
        self.conn.commit()
