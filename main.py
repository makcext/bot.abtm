import asyncio
import random
import logging
import signal
from config import DELAY_MIN, DELAY_MAX
from reddit_client import download_new_posts
from telegram_client import create_bot
from data_manager import load_last_timestamp, save_last_timestamp
from post_processor import process_posts

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    last_run_timestamp = load_last_timestamp()
    downloaded_posts, new_last_timestamp = await download_new_posts(last_run_timestamp)
    
    bot = create_bot()
    if bot:
        await process_posts(downloaded_posts, bot)
    else:
        logging.error("BOT_TOKEN is not set")
    save_last_timestamp(new_last_timestamp)

async def shutdown(signal, loop):
    logging.info(f"Получен сигнал {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(s, loop))
        )
    
    run = True
    try:
        while run:
            try:
                loop.run_until_complete(main())
                delay = random.randint(DELAY_MIN, DELAY_MAX)
                logging.info(f"Sleeping for {delay} seconds")
                loop.run_until_complete(asyncio.sleep(delay))
            except asyncio.CancelledError:
                run = False
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        logging.info("Успешно завершено!")