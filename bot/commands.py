from math import log
from turtle import up
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import logging

from tomlkit import key
from mock.mock_country_api import get_countries, get_services, generate_mock_data

from models import user
import services

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

httpx_logger = logging.getLogger('httpx')

# Set the logging level to WARNING so INFO level logs are not shown
httpx_logger.setLevel(logging.WARNING)



# Определяем состояния
SELECT_ACTION, SELECT_COUNTRY, SELECT_SERVICE, SHOW_NUMBERS, ORDER_DETAILS = range(5)

# Функция приветствия и начала работы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        await update.message.reply_text(
            "Привет! Я помогу вам найти идеальный мобильный номер. "
            "Начнем! Вы хотите выбрать страну или сервис?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Страна", callback_data='country')],
                [InlineKeyboardButton("Сервис", callback_data='service')],
            ]),
        )
    else:
        logging.info("Update is not a message")
    return SELECT_ACTION

# Обработка выбора страны или сервиса
async def select_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logging.info("select_action function started")
    query = update.callback_query
    await query.answer()
    action = query.data
    logging.info(f"Action: {action}")

    if action == 'country':
        # context.user_data['selected_service'] = None  # Очищаем предыдущий выбор сервиса
        countries = await get_countries()
        keyboard = [[InlineKeyboardButton(country, callback_data=country)] for country in countries]
        await query.edit_message_text("Выберите страну:", reply_markup=InlineKeyboardMarkup(keyboard))

        # Log the selected country
        selected_country = context.user_data.get('selected_country')
        
        logging.info(f"Selected country: {selected_country}")

        return SELECT_COUNTRY
    
    else:
        # context.user_data['selected_country'] = None  # Очищаем предыдущий выбор страны
        services = await get_services()
        keyboard = [[InlineKeyboardButton(service, callback_data=service)] for service in services]
        await query.edit_message_text("Выберите сервис:", reply_markup=InlineKeyboardMarkup(keyboard))
        return SELECT_SERVICE


#Переход к выбору страны, если изначально выбран сервис, и наоборот
async def select_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    country = query.data  # Получаем выбранную страну
    context.user_data['selected_country'] = country  # Сохраняем выбор страны
    
    logging.info(f"Selected country: {country}")

    services = await get_services()
    keyboard = [[InlineKeyboardButton(service, callback_data=service)] for service in services]
    await query.edit_message_text("Выберите сервис:", reply_markup=InlineKeyboardMarkup(keyboard))
    logging.info(f"Selected country: {country}")

    return SHOW_NUMBERS

async def select_service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    service = query.data  # Получаем выбранный сервис
    context.user_data['selected_service'] = service  # Сохраняем выбор сервиса
    
    logging.info(f"Selected service: {service}")

    countries = await get_countries()
    keyboard = [[InlineKeyboardButton(country, callback_data=country)] for country in countries]
    await query.edit_message_text("Выберите страну:", reply_markup=InlineKeyboardMarkup(keyboard))
    logging.info(f"Selected service: {service}")

    return SHOW_NUMBERS


# Предложение номеров и оформление заказа
async def show_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Здесь логика для отображения доступных номеров
    numbers = await generate_mock_data()
    #filter by country and service from prev choises
    country = 'USA'
    service = 'Apple'
    filtered_numbers = [number for c, s, number in numbers if c == country and s == service]
    logging.info(f"Filtered numbers: {filtered_numbers}")
    
    keyboard = [[InlineKeyboardButton(number, callback_data=number)] for number in filtered_numbers]
    await update.callback_query.edit_message_text("Выберите номер:", reply_markup=InlineKeyboardMarkup(keyboard))

    return ORDER_DETAILS

async def order_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Здесь логика для оформления заказа
    await update.message.reply_text("Заказ оформлен. Спасибо!")
    return ConversationHandler.END

# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Разговор окончен.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END