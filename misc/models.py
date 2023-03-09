import dataclasses
import datetime


@dataclasses.dataclass
class SourceItem:
    id: int
    link: str
    photo: str
    name: str
    price: float
    creation_date: datetime.datetime


@dataclasses.dataclass
class MarketPlaceItem:
    id: int
    link: str
    photo: str
    name: str
    price: float
    source_item: SourceItem


@dataclasses.dataclass
class SecretInfo:
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DBNAME: str
    TELEGRAM_BOT_TOKEN: str
    ADMIN_LIST: list[int]
    IS_SERVER: str


@dataclasses.dataclass
class ExcelImportStats:
    inserted_count: int
    positions_count: int
    from_file_count: int
