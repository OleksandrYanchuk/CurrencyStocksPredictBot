import logging
import os
import json
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from currency_stock_data.labels import currency, stock_tickers

from dotenv import load_dotenv


load_dotenv()

# Функція для завантаження даних з JSON-файлу
def load_currency_data():
    file_name = (
        f"currency_stock_data/currency_predictions_{datetime.today().date()}.json"
    )
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    return data


def load_stock_data():
    file_name = f"currency_stock_data/stock_predictions_{datetime.today().date()}.json"
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    return data


def load_stock_data_week():
    file_name = (
        f"currency_stock_data/stock_predictions_week_{datetime.today().date()}.json"
    )
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    return data


def load_stock_data_month():
    file_name = (
        f"currency_stock_data/stock_predictions_month_{datetime.today().date()}.json"
    )
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    return data


def load_currency_data_analys():
    file_name = f"currency_stock_data/currency_analysis_results.json"
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    return data


def load_stock_data_analys():
    file_name = f"currency_stock_data/stock_analysis_results.json"
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    return data


API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
button_currency = KeyboardButton("Currency")
button_stocks = KeyboardButton("Stocks")
button_currency_analyse = KeyboardButton("Analyse_currency")
button_stocks_analyse = KeyboardButton("Analyse_stocks")
markup.add(
    button_currency, button_stocks, button_currency_analyse, button_stocks_analyse
)

items_per_page = 15

current_page = 1

previous_day = datetime.today().date() - timedelta(days=1)

currency_pairs = currency
stocks = stock_tickers
global user_choice
user_choice = None

currency_keyboard = InlineKeyboardMarkup()
for pair in currency_pairs:
    currency_keyboard.add(InlineKeyboardButton(text=pair, callback_data=f"pair_{pair}"))

stocks_keyboard = InlineKeyboardMarkup()
for stock in stocks:
    stocks_keyboard.add(
        InlineKeyboardButton(text=stock, callback_data=f"stock_{stock}")
    )


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! Це твій бот. Вибери, що ти хочеш передбачити:", reply_markup=markup
    )


@dp.message_handler(lambda message: message.text in ["Currency", "Stocks"])
async def process_user_choice(message: types.Message):
    global user_choice
    user_choice = message.text

    if user_choice == "Currency":
        await message.answer("Обери валютну пару:", reply_markup=currency_keyboard)
    elif user_choice == "Stocks":
        await show_stocks_page(message, current_page)
    elif user_choice == "Analyse_currency":
        await show_currency_analys_page(message, current_page)
    elif user_choice == "Analyse_stocks":
        await show_stocks_analys_page(message, current_page)


@dp.callback_query_handler(lambda query: query.data.startswith("pair_"))
async def process_currency_choice(query: types.CallbackQuery):
    selected_pair = query.data.replace("pair_", "")

    # Завантажте дані з JSON-файлу
    currency_data = load_currency_data()

    # Отримайте ціну закриття для обраної валютної пари
    if selected_pair in currency_data:
        closing_price = currency_data[selected_pair]
        message_text = f"Орієнтовна ціна закриття на {datetime.today().date()} валютної пари ({selected_pair}): {closing_price}"
    else:
        message_text = f"Дані для валютної пари ({selected_pair}) не знайдено."

    await query.message.answer(message_text)

    # Закрийте вікно з вибором валютної пари
    await query.message.delete()


async def show_stocks_page(message, page):
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_stocks = stocks[start_index:end_index]

    stocks_keyboard = InlineKeyboardMarkup()
    for stock in current_stocks:
        stocks_keyboard.add(
            InlineKeyboardButton(text=stock, callback_data=f"stock_{stock}")
        )

    pagination_keyboard = InlineKeyboardMarkup()
    if page > 1:
        pagination_keyboard.add(
            InlineKeyboardButton(text="← Previous", callback_data="prev_page")
        )
    if end_index < len(stocks):
        pagination_keyboard.add(
            InlineKeyboardButton(text="Next →", callback_data="next_page")
        )

    await message.answer("Обери акцію:", reply_markup=stocks_keyboard)
    await message.answer("Пагінація:", reply_markup=pagination_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith("stock_"))
async def process_stock_choice(query: types.CallbackQuery):
    selected_stock = query.data.replace("stock_", "")
    stock_data = load_stock_data()
    stock_data_week = load_stock_data_week()
    stock_data_month = load_stock_data_month()
    if selected_stock in stock_data:
        closing_price_day = stock_data[selected_stock]
        closing_price_week = stock_data_week[selected_stock]
        closing_price_month = stock_data_month[selected_stock]

        message_text = (
            f"Орієнтовна ціна закриття на {datetime.today().date()} акції ({selected_stock}): {closing_price_day}\n"
            f"на тиждень {closing_price_week}\n"
            f"на місяць {closing_price_month}"
        )
    else:
        message_text = f"Дані для акції ({selected_stock}) не знайдено."

    await query.message.answer(message_text)

    # Закрийте вікно з вибором валютної пари
    await query.message.delete()


@dp.message_handler(
    lambda message: message.text in ["Analyse_currency", "Analyse_stocks"]
)
async def process_analyse_choice(message: types.Message):
    global user_choice
    user_choice = message.text

    if user_choice == "Analyse_currency":
        await show_currency_analys_page(message, current_page)
    elif user_choice == "Analyse_stocks":
        await show_stocks_analys_page(message, current_page)


async def show_currency_analys_page(message, page):
    # Завантажте результати аналізу валютних пар
    currency_analys_data = load_currency_data_analys()

    # Створіть повідомлення з результатами аналізу для поточної сторінки
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_currency_pairs = list(currency_analys_data.keys())[start_index:end_index]
    currency_analys_message = f"Результати аналізу валютних пар за {previous_day}:\n"

    for currency_pair in current_currency_pairs:
        analysis_data = currency_analys_data[currency_pair]
        rmse = analysis_data.get("RMSE", "N/A")
        mae = analysis_data.get("MAE", "N/A")
        actual_change = analysis_data.get("actual_change", "N/A")
        predict_change = analysis_data.get("predict_change", "N/A")

        currency_analys_message += f"{currency_pair}\n"
        currency_analys_message += f"RMSE: {rmse}\n"
        currency_analys_message += f"MAE: {mae}\n"
        currency_analys_message += f"Actual Change: {actual_change}\n"
        currency_analys_message += f"Predicted Change: {predict_change}\n\n"

    await message.answer(currency_analys_message)

    # Побудуйте клавіатуру пагінації
    pagination_keyboard = InlineKeyboardMarkup()
    if page > 1:
        pagination_keyboard.add(
            InlineKeyboardButton(
                text="← Previous", callback_data="prev_page_analys_currency"
            )
        )
    if end_index < len(currency_analys_data):
        pagination_keyboard.add(
            InlineKeyboardButton(
                text="Next →", callback_data="next_page_analys_currency"
            )
        )

    await message.answer("Пагінація:", reply_markup=pagination_keyboard)


async def show_stocks_analys_page(message, page):
    # Завантажте результати аналізу акцій
    stocks_analys_data = load_stock_data_analys()

    # Створіть повідомлення з результатами аналізу для поточної сторінки
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_stocks = list(stocks_analys_data.keys())[start_index:end_index]
    stocks_analys_message = f"Результати аналізу акцій за {previous_day}:\n"

    for stock in current_stocks:
        analysis_data = stocks_analys_data[stock]
        rmse = analysis_data.get("RMSE", "N/A")
        mae = analysis_data.get("MAE", "N/A")
        actual_change = analysis_data.get("actual_change", "N/A")
        predict_change = analysis_data.get("predict_change", "N/A")

        stocks_analys_message += f"{stock}\n"
        stocks_analys_message += f"RMSE: {rmse}\n"
        stocks_analys_message += f"MAE: {mae}\n"
        stocks_analys_message += f"Actual Change: {actual_change}\n"
        stocks_analys_message += f"Predicted Change: {predict_change}\n\n"

    await message.answer(stocks_analys_message)

    # Побудуйте клавіатуру пагінації
    pagination_keyboard = InlineKeyboardMarkup()
    if page > 1:
        pagination_keyboard.add(
            InlineKeyboardButton(
                text="← Previous", callback_data="prev_page_analys_stocks"
            )
        )
    if end_index < len(stocks_analys_data):
        pagination_keyboard.add(
            InlineKeyboardButton(text="Next →", callback_data="next_page_analys_stocks")
        )

    await message.answer("Пагінація:", reply_markup=pagination_keyboard)


@dp.callback_query_handler(lambda query: query.data == "prev_page")
async def process_previous_page(query: types.CallbackQuery):
    global current_page
    if current_page > 1:
        current_page -= 1
    await query.answer()
    await show_stocks_page(query.message, current_page)


@dp.callback_query_handler(lambda query: query.data == "next_page")
async def process_next_page(query: types.CallbackQuery):
    global current_page
    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page
    if end_index < len(stocks):
        current_page += 1
    await query.answer()
    await show_stocks_page(query.message, current_page)


@dp.callback_query_handler(lambda query: query.data == "prev_page_analys_currency")
async def process_previous_page_analys_currency(query: types.CallbackQuery):
    global current_page
    if current_page > 1:
        current_page -= 1
    await query.answer()
    await show_currency_analys_page(query.message, current_page)


@dp.callback_query_handler(lambda query: query.data == "next_page_analys_currency")
async def process_next_page_analys_currency(query: types.CallbackQuery):
    global current_page
    current_page += 1
    await query.answer()
    await show_currency_analys_page(query.message, current_page)


@dp.callback_query_handler(lambda query: query.data == "prev_page_analys_stocks")
async def process_previous_page_analys_stocks(query: types.CallbackQuery):
    global current_page
    if current_page > 1:
        current_page -= 1
    await query.answer()
    await show_stocks_analys_page(query.message, current_page)


@dp.callback_query_handler(lambda query: query.data == "next_page_analys_stocks")
async def process_next_page_analys_stocks(query: types.CallbackQuery):
    global current_page
    current_page += 1
    await query.answer()
    await show_stocks_analys_page(query.message, current_page)


if __name__ == "__main__":
    from aiogram import executor

    # Check if the script is being run directly
    if __name__ == "__main__":
        executor.start_polling(dp, skip_updates=True)
