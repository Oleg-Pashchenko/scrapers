import psycopg2

from misc.models import SourceItem, MarketPlaceItem
from misc.secrets import secret_info


class MarketPlaceScraper:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.conn = psycopg2.connect(
            host=secret_info.POSTGRES_HOST,
            database=secret_info.POSTGRES_DBNAME,
            user=secret_info.POSTGRES_USER,
            password=secret_info.POSTGRES_PASSWORD,
        )
        self.cur = self.conn.cursor()

    def get_source_item(self):
        self.cur.execute(f"SELECT * FROM {self.table_name}", ())
        record = self.cur.fetchone()
        if record:
            self.delete_source_item(record[0])
            return SourceItem(
                id=record[0],
                link=record[1],
                photo=record[2],
                name=record[3],
                price=record[4],
                creation_date=record[5],
            )
        return None

    def delete_source_item(self, id):
        self.cur.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (id,))
        self.conn.commit()

    def save_to_error_mk(self, table_name, source_item: SourceItem, now):
        self.cur.execute(
            f"""INSERT INTO {table_name} (id, link, photo, name, price, creation_date, check_date) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                source_item.id,
                source_item.link,
                source_item.photo,
                source_item.name,
                source_item.price,
                source_item.creation_date,
                now,
            ),
        )
        self.conn.commit()

    def save_to_neural(self, table_name, mk_item: MarketPlaceItem):
        data = mk_item.source_item
        self.cur.execute(
            f"""INSERT INTO {table_name} (id, link, photo, name, 
        price, source_id, source_link, source_photo, source_name, source_price, source_creation_date)
                 SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM {table_name} WHERE id=%s)""",
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
