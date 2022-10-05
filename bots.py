import os

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from services import start, message, most_expensive, most_popular, popular_products

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))  # catch command "/start"
    app.add_handler(MessageHandler(~filters.COMMAND, message))  # catch all messages except commands
    app.add_handler(CommandHandler("most_expensive",
                                   most_expensive))  # catch command "/most_expensive"
    app.add_handler(CommandHandler("most_popular",
                                   most_popular))  # catch command "/most_popular"
    app.add_handler(CommandHandler("popular_products",
                                   popular_products))  # catch command "/most_popular"
    app.run_polling()
