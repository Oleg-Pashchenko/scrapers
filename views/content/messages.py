import requests
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from PIL import Image
from db.presentation import PresentationScraper

HELLO_MESSAGE = (
    "Привет!\nЭтот бот предназначен для проверки и загрузки товаров на Ozon / Wilberries от поставщиков."
    "\nЛогика взаимодействия простая:\n1) Нажимаете посмотреть карточку, далее, если товары соответствуют,"
    "нажимаете на кнопку `Принять`, иначе - `Отклонить`."
)
ADMIN_MESSAGE = (
    "(Это сообщение видят только админы)\nДля добавления новых кодов товара загрузите XLSX файл, где "
    "в столбце A со 2 строчки будут указаны коды товара. "
    "\nЗаметьте, код товара - именно число, без дополнительных символов)\n"
    "В противном случае товар принят не будет!"
)
presentation_scraper = PresentationScraper()


def download_image(link: str, index):
    filename = f"{index}.jpg"
    img_data = requests.get(link).content
    with open(filename, "wb") as handler:
        handler.write(img_data)
    handler.close()
    image = Image.open(filename)
    sunset_resized = image.resize((250, 250))
    sunset_resized.save(filename)
    return filename


update_btn = ReplyKeyboardMarkup(resize_keyboard=True)
update_btn.add(KeyboardButton("Обновить"))


def get_content():
    item = presentation_scraper.get_item()
    message = (
        f"""<b>Данные из маркетплейса:\nID:</b> {item.id}\n<b>Цена:</b> {item.price}\n<b>Название:</b> """
        f"""{item.name.strip()}\n<a href="{item.link}">Посмотреть товар</a>\n"""
        f"""----------------------------------------------------\n<b>Данные из источника:\nID:</b> {item.source_item.id}\n<b>Цена:</b> {item.source_item.price}\n"""
        f"""<b>Название:</b> {item.source_item.name.strip()}\n<a href="{item.source_item.link}">Посмотреть товар</a>
    """
    )
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("✅", callback_data=f"yes_{item.id}")
    button2 = InlineKeyboardButton("❌", callback_data=f"no_{item.id}")
    markup.add(button1, button2)
    img1, img2 = download_image(item.photo, 1), download_image(
        item.source_item.photo, 2
    )
    img1 = InputMediaPhoto(open(img1, "rb"), caption="Marketplace")
    img2 = InputMediaPhoto(open(img2, "rb"), caption="Source")
    return message, markup, img1, img2
