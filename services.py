import aiohttp
import aioredis
import logging
import os
from telegram import Bot, Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

redis = aioredis.from_url("redis://localhost")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    logger.info(
        f"Reply to command '/start' (User={first_name} {last_name}, Chat ID={update.effective_chat.id})")

    await redis.lpush("chats", update.effective_chat.id)
    chat_ids = set()
    chat_len = await redis.llen("chats")
    for index in range(chat_len):
        chat_id = await redis.lindex("chats", index)
        chat_ids.add(chat_id.decode())
        print(chat_ids)
    await update.message.reply_text(f"Start {update.effective_user.first_name}")


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    logger.info(
        f"Reply to message '{update.message.text}' (User={first_name} {last_name}, Chat ID={update.effective_chat.id})")
    await update.message.reply_text(f"Message {update.effective_user.first_name}")


async def send_message(text: str, chat_id: int) -> None:
    logger.info(f"Send message '{text}'")
    bot = Bot(os.environ.get("BOT_TOKEN"))
    await bot.send_message(chat_id=chat_id, text=text)


async def most_expensive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    logger.info(
        f"Reply to command '/most_expensive' (User={first_name} {last_name}, Chat ID={update.effective_chat.id})")
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/api/products/?ordering=-cost") as response:
            product_list = await response.json()
    result = ""
    for i, product in enumerate(product_list["results"], 1):
        result += f"{i}) {product['title']} (Cost={product['cost']})\n"
    await update.message.reply_text(f"Top 10 most expensive products:\n{result}")


async def most_popular(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    logger.info(
        f"Reply to command '/most_expensive' (User={first_name} {last_name}, Chat ID={update.effective_chat.id})")
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/api/products/?ordering=-popular") as response:
            product_list = await response.json()
    result = ""
    for i, product in enumerate(product_list["results"], 1):
        result += f"{i}) {product['title']} (Cost={product['cost']})\n"
    await update.message.reply_text(f"Top 10 most popular products:\n{result}")


async def popular_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    logger.info(
        f"Reply to command '/popular_products' (User={first_name} {last_name}, Chat ID={update.effective_chat.id})")
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/api/purchases/sold") as response:
            product_list = await response.json()
    result = ""
    for i, product in enumerate(product_list["results"], 1):
        result += f"{i}) {product['title']} (Sold={product['sold']})\n"
    await update.message.reply_text(f"The popular products:\n{result}")
