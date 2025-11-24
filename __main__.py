from pyrogram import Client as Bot

from callsmusic import run
from config import API_HASH, API_ID, BOT_TOKEN


if __name__ == "__main__":
    Bot(
        ":memory:",
        API_ID,
        API_HASH,
        bot_token=BOT_TOKEN,
        plugins={"root": "callsmusic.handlers"},
    ).start()

    run()
