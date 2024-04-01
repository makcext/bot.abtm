import logging
from telegram.ext import Application
from bot.conversation_handlers import conv_handler
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.BASIC_FORMAT
)
logger = logging.getLogger(__name__)

def main():
    application = Application.builder().token("6735927791:AAEtA7jjgR7WJXL0ZW1tmt-Dpd42ORzMZxA").build()

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()