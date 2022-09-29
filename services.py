import logging
import os

import aiohttp
from telegram import Bot

from telegram import Update
from telegram.ext import ContextTypes

# from queries import get_most_expensive, get_most_popular

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    logger.info(
        f"Reply to command '/start' (User={first_name} {last_name}, Chat ID={update.effective_chat.id})")
    await update.message.reply_text(f"Start {update.effective_user.first_name}")


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    logger.info(
        f"Reply to message '{update.message.text}' (User={first_name} {last_name}, Chat ID={update.effective_chat.id})")
    await update.message.reply_text(f"Message {update.effective_user.first_name}")


async def send_message(text: str) -> None:
    logger.info(f"Send message '{text}'")
    bot = Bot(os.environ.get("BOT_TOKEN"))
    await bot.send_message(chat_id=os.environ.get("CHAT_ID"), text=text)


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
