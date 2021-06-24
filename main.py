import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from Constants import bot_key
from news_parser import check_news_update

bot = Bot(token=bot_key,  parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все новости", "Последние 5 новостей", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Лента новостей", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):

        news =f"<b>{(v['section_title'])}</b>\n\n" \
                f"{(v['section_url'])}\n" \


        await message.answer(news)


@dp.message_handler(Text(equals="Последние 5 новостей"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"<b>{(v['section_title'])}</b>\n\n" \
               f"{(v['section_url'])}\n" \


        await message.answer(news)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"<b>{(v['section_title'])}</b>\n\n" \
                   f"{(v['section_url'])}\n" \


            await message.answer(news)

    else:
        await message.answer("Пока нет свежих новостей...")


if __name__ == '__main__':
    executor.start_polling(dp)
