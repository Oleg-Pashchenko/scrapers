import json

import dotenv
import os

from misc.models import SecretInfo


def load_secrets() -> SecretInfo:
    dotenv.load_dotenv()
    admins = os.getenv("ADMIN_LIST")
    admin_list = []
    try:
        admin_list = json.loads(admins)
    except:
        pass
    return SecretInfo(
        POSTGRES_USER=os.getenv("POSTGRES_USER"),
        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
        POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
        POSTGRES_PORT=os.getenv("POSTGRES_PORT"),
        POSTGRES_DBNAME=os.getenv("POSTGRES_DBNAME"),
        TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN"),
        ADMIN_LIST=admin_list,
        IS_SERVER=os.getenv("IS_SERVER"),
    )


secret_info = load_secrets()
