import logging
from bot_token import bot_token
from text_content import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.types import InputFile

bot = Bot(token=bot_token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# presentation = InputFile("content/eBook.pdf")  # отправка файла напрямую
# TODO: добавить кнопки с вопросами в стиле игры


@dp.message_handler(commands="start")
@dp.message_handler(lambda message: message.text == "🔙")  # main keyboard
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = BUTTONS_MAIN
    keyboard.add(*buttons)
    await message.answer("<u>Черногория. Горы в зеркале Адриатики</u>", parse_mode="HTMl")
    await message.answer("Dobrodošli!\nЭтот бот поможет ознакомится вам с книгой о Черногории. ↓",
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in BUTTONS_MAIN)  # main keyboard' buttons handler
async def main_buttons(message: types.Message):
    try:
        if message.text == BUTTONS_MAIN[0]:
            buttons = [types.InlineKeyboardButton(text=BUTTONS_BOOK[i],
                                                  callback_data=BUTTONS_BOOK[i]) for i in range(len(BUTTONS_BOOK))]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await message.answer("Выберите, что вас интересует: ↓", reply_markup=keyboard)
        elif message.text == BUTTONS_MAIN[1]:
            await message.answer(text="Муцевич Адалета, студент Москвоского Политехнического "
                                      "Университета и любитель балканских стран.")
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(types.InlineKeyboardButton(text="Адалета на Bēhance",
                                                    url="https://www.behance.net/adaletamutsevi"))
            await message.answer(text="@Mutsv_A", reply_markup=keyboard)
        elif message.text == BUTTONS_MAIN[2]:  # TODO: загрузить финальный ролик на ютуб и добавить сюда ссылку
            await message.answer(text="*тут будет ссылка на ютуб ролик*")
        elif message.text == BUTTONS_MAIN[3]:  # TODO: загрузить финальную пдфку на гугл диск и добавить сюда ссылку
            await message.answer(text="Перейдите по ссылке↓\n*тут будет ссылка на гугл док*")
            # await bot.send_document(document=presentation, chat_id=message.chat.id)
        elif message.text == BUTTONS_MAIN[4]:
            buttons = [types.InlineKeyboardButton(text="Купить на Ozon", url="https://www.ozon.ru/product/"
                                                                             "chernogoriya-gory-v-zerkale-adriatiki"
                                                                             "-raskina-elena-yurevna-kozhemyakin-"
                                                                             "mihail-vladimirovich-255663281/"),
                       types.InlineKeyboardButton(text="Купить в Лабиринте", url="https://www.labirint.ru/"
                                                                                 "books/375420/")]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await message.answer("Ссылки на разные интернет магазины", reply_markup=keyboard)
    except IndexError as ie:  # Если забыли изменить код после редактирования кол-ва кнопок
        await message.answer("Нет доступа к этой части!\nПопробуйте позже.")
        print(f"[ERROR]: {ie}")


@dp.callback_query_handler(lambda c: c.data in BUTTONS_BOOK)  # handles callback keyboard about book
async def book_buttons(call: types.CallbackQuery):
    try:
        if call.data == BUTTONS_BOOK[0]:
            await call.answer(text=SHORT_INFO, show_alert=True)
        elif call.data == BUTTONS_BOOK[1]:
            await call.answer()
            try:
                photos = [InputFile("content/kotor.png"), InputFile("content/map.png"),
                          InputFile("content/perast.png"), InputFile("content/zmajevic.png")]
                await call.message.answer("Moć dizajna ↓")
                for i in photos:
                    await bot.send_document(document=i, chat_id=call.message.chat.id)
            except FileNotFoundError as fe:
                await call.message.answer("Не получилось найти изображеня")
                print(f"[ERROR]: {fe}")
        elif call.data == BUTTONS_BOOK[2]:
            buttons = [types.InlineKeyboardButton(text=BUTTONS_NAVIGATION[i],
                                                  callback_data=BUTTONS_NAVIGATION[i])
                       for i in range(len(BUTTONS_NAVIGATION))]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await call.answer()
            await call.message.answer("Узнайте, где в книге найти данные темы: ↓", reply_markup=keyboard)
        elif call.data == BUTTONS_BOOK[3]:
            buttons = ["🔙"] + [str(i) for i in range(1, len(BUTTONS_CITIES) + 1)]
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
            keyboard.add(*buttons)
            await call.answer()
            await call.message.answer(
                "\n".join([str(i + 1) + ") " + list(BUTTONS_CITIES)[i] for i in range(len(BUTTONS_CITIES))]))
            await call.message.answer("Выберите город/достопримечательность на клавиатуре ↓", reply_markup=keyboard)
    except IndexError as ie:  # Если забыли изменить код после редактирования кол-ва кнопок
        await call.message.answer("Нет доступа к этой части!\nПопробуйте позже.")
        await call.answer()
        print(f"[ERROR]: {ie}")


@dp.callback_query_handler(lambda c: c.data in BUTTONS_NAVIGATION)  # handles callback buttons about book navigation
async def navigation_buttons(call: types.CallbackQuery):
    try:
        await call.answer(text=NAVIGATION_INFO[BUTTONS_NAVIGATION.index(call.data)], show_alert=True)
    except IndexError as ie:  # Если забыли изменить код после редактирования кол-ва кнопок
        await call.message.answer("Нет доступа к этой части!\nПопробуйте позже.")
        print(f"[ERROR]: {ie}")


# respond to an index of some place in list BUTTONS_CITIES
@dp.message_handler(lambda message: message.text in [str(i + 1) for i in range(len(BUTTONS_CITIES))])
async def cities_buttons(message: types.Message):
    cities_list = BUTTONS_CITIES[list(BUTTONS_CITIES)[int(message.text) - 1]]
    await message.answer(f"<b>{list(BUTTONS_CITIES)[int(message.text) - 1]}</b>", parse_mode="HTMl")
    await message.answer(f"Смотрите следующие страницы:\n{cities_list[0]}") if cities_list[0] else \
        await message.answer("Пока что в книге не упоминается это место")
    if len(cities_list) > 1:
        buttons = [types.InlineKeyboardButton(text=f"Статья {i}",
                                              url=cities_list[i]) for i in range(1, len(cities_list))]
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*buttons)
        await message.answer("Вот несколько отличных статей для подробного ознакомления:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text not in BUTTONS_BOOK + BUTTONS_MAIN)  # respond to random message.text
async def normal_text_response(message: types.Message):
    await message.reply("Ne razumijem te!\nПолзуйтесь кнопками. ↓")


@dp.errors_handler(exception=BotBlocked)  # if user blocked bot while he is processing some request
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True


if __name__ == "__main__":
    # run
    executor.start_polling(dp, skip_updates=True)
