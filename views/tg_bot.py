import asyncio
import datetime

from db.managers import ManagersScraper
from db.presentation import PresentationScraper
from misc import excel_import

from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType

from misc.secrets import secret_info
from views.content import messages
from views.content.messages import get_content

TOKEN = secret_info.TELEGRAM_BOT_TOKEN
ADMIN_LIST = secret_info.ADMIN_LIST
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
presentation_scraper = PresentationScraper()
managers_scraper = ManagersScraper()


async def delete_prev_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id - 2)


async def send_question(message):
    message_text, buttons, image_1, image_2 = get_content()
    await bot.send_media_group(message.chat.id, media=[image_1, image_2])
    try:
        await bot.send_message(
            message.chat.id, message_text, reply_markup=buttons, parse_mode="HTML"
        )
    except:
        await bot.send_message(
            message.chat.id, "Описание отсутствует", reply_markup=buttons
        )


async def add_to_execute(data):
    user = managers_scraper.get_user(data.message.chat.id)
    if not str(datetime.datetime.now().date()) in user.history.keys():
        user.history[str(datetime.datetime.now().date())] = 0
    user.history[str(datetime.datetime.now().date())] += 1
    managers_scraper.update_user(user)
    await data.answer("Добавлено!")
    await delete_prev_message(data.message)
    presentation_scraper.write_result(data.data.split("_")[1])
    presentation_scraper.delete_item(data.data.split("_")[1])
    await send_question(data.message)


async def remove_from_order(data):
    await data.answer("Удалено!")
    await delete_prev_message(data.message)
    presentation_scraper.write_error(data.data.split("_")[1])
    presentation_scraper.delete_item(data.data.split("_")[1])
    await send_question(data.message)


async def handle_document(message: types.Message):
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    with open("test.xlsx", "wb") as f:
        f.write(downloaded_file.read())
    f.close()
    statistic = excel_import.load_excel_to_db("test.xlsx")
    await bot.send_message(
        message.chat.id,
        f"Файл обработан:\nСтрок в файле: {statistic.from_file_count}"
        f"\nКорректных строк: {statistic.positions_count}"
        f"\nДобавлено в базу (новых): {statistic.inserted_count}",
    )


async def handle_messages(message: types.Message):
    if message.text == "/stats":
        users = managers_scraper.get_statistic()
        response = "Статистика за сегодня:"
        for user in users:
            if str(datetime.datetime.now().date()) in user.history.keys():
                response += (
                    f"\n{user.name}: {user.history[str(datetime.datetime.now().date())]}"
                )
        await message.answer(response)
    if message.text == "Обновить":
        await send_question(message)
    if message.text == "/start":
        if not managers_scraper.get_user(message.chat.id):
            managers_scraper.add_user(
                message.chat.id, f"{message.chat.first_name} {message.chat.last_name}"
            )
        await bot.send_message(
            message.chat.id, messages.HELLO_MESSAGE, reply_markup=messages.update_btn
        )
        if message.chat.id in ADMIN_LIST:
            await bot.send_message(message.chat.id, messages.ADMIN_MESSAGE)
        await send_question(message)


def tg_bot():
    dp.register_message_handler(handle_messages)
    dp.register_message_handler(
        handle_document, content_types=[types.ContentType.DOCUMENT]
    )
    dp.register_callback_query_handler(add_to_execute, lambda m: "yes" in m.data)
    dp.register_callback_query_handler(remove_from_order, lambda m: "no" in m.data)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(dp.start_polling())
