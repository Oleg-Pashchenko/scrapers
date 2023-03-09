import json

import psycopg2

from misc.models import User
from misc.secrets import secret_info


class ManagersScraper:
    def __init__(self):
        self.table_name = "managers"
        self.conn = psycopg2.connect(
            host=secret_info.POSTGRES_HOST,
            database=secret_info.POSTGRES_DBNAME,
            user=secret_info.POSTGRES_USER,
            password=secret_info.POSTGRES_PASSWORD,
        )
        self.cur = self.conn.cursor()

    def update_user(self, user: User):
        self.cur.execute(
            f"UPDATE {self.table_name} SET history = %s WHERE id = %s",
            (
                json.dumps(user.history),
                user.id,
            ),
        )
        self.conn.commit()

    def add_user(self, id, name):
        self.cur.execute(
            f"""INSERT INTO {self.table_name} (id, name, history) VALUES (%s, %s, %s)""",
            (
                id,
                name,
                json.dumps({}),
            ),
        )
        self.conn.commit()

    def get_user(self, id):
        self.cur.execute(f"SELECT * FROM {self.table_name} WHERE id = %s", (id,))
        record = self.cur.fetchone()
        if record:
            return User(id=record[0], name=record[1], history=json.loads(record[2]))
        else:
            return None

    def get_statistic(self):
        self.cur.execute(f"SELECT * FROM {self.table_name}", ())
        records = self.cur.fetchall()
        users = []

        for record in records:
            users.append(
                User(id=record[0], name=record[1], history=json.loads(record[2]))
            )
        return users
