import psycopg2
from misc.secrets import secret_info


class SourceScraper:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.conn = psycopg2.connect(
            host=secret_info.POSTGRES_HOST,
            database=secret_info.POSTGRES_DBNAME,
            user=secret_info.POSTGRES_USER,
            password=secret_info.POSTGRES_PASSWORD,
        )
        self.cur = self.conn.cursor()

    def get_code(self):
        self.cur.execute(f"SELECT * FROM {self.table_name}", ())
        record = self.cur.fetchone()
        if record:
            self.delete_code(record[0])
            return record[0], record[1]
        return None, None

    def delete_code(self, id):
        self.cur.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (id,))
        self.conn.commit()

    def insert_into_source_table(self, position, now):
        self.cur.execute(
            f"""INSERT INTO {self.table_name} (id, upload_date)
         SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM {self.table_name} WHERE id=%s)""",
            (position, now, position),
        )
        self.conn.commit()

    def insert_count_by_date(self, timestamp):
        self.cur.execute(
            f"""SELECT id FROM {self.table_name} WHERE upload_date=%s""", (timestamp,)
        )
        data = self.cur.fetchall()
        return len(data)

    def save_to_error_db(self, table_name, code, date, now):
        self.cur.execute(
            f"""INSERT INTO {table_name} (id, upload_date, check_date) VALUES (%s, %s, %s)""",
            (
                code,
                date,
                now,
            ),
        )
        self.conn.commit()

    def save_to_mk(self, table_name, data):
        data.name = self.prepare_name_to_mk(data.name)
        self.cur.execute(
            f"""INSERT INTO {table_name} (id, link, photo, name, price, creation_date)
         SELECT %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM {table_name} WHERE id=%s)""",
            (
                data.id,
                data.link,
                data.photo,
                data.name,
                data.price,
                data.creation_date,
                data.id,
            ),
        )
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def prepare_name_to_mk(self, name):
        name = name.split()
        digits = '1234567890'
        alphabet_to_delete = 'abcdefghijklmnopqrstuvwxyz' + digits
        new_name = []
        for word in name:
            if word.isdigit() and len(word) > 4:
                continue
            if 'арт.' in word:
                continue
            if 'г.' in word:
                continue
            delete_it = True
            for symbol in word.lower():
                if symbol not in alphabet_to_delete:
                    delete_it = False
                    break

            is_str_contain_digits = False
            for symbol in word.lower():
                if symbol in digits:
                    is_str_contain_digits = True
                    break

            if delete_it and is_str_contain_digits and len(word) > 5:
                continue
            new_name.append(word)
        return ' '.join(new_name)
