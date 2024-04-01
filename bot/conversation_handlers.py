from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from .commands import *

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        SELECT_ACTION: [CallbackQueryHandler(select_action)],
        SELECT_COUNTRY: [CallbackQueryHandler(select_country)],
        SELECT_SERVICE: [CallbackQueryHandler(select_service)],
        SHOW_NUMBERS: [CallbackQueryHandler(show_numbers)],
        ORDER_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_details)],
    },
    fallbacks=[CommandHandler("cls", cancel)],
    per_message=False,
)