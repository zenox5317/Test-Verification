from os import getenv
from pyrogram import Client, filters
import random
import string
import time
import requests
from urllib.parse import quote

API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
SHORTNER = getenv("SHORTNER", "")
API = getenv("API", "")

vrfybot = Client("vrfybot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, workers=500, in_memory=True)

VERIFIED_USERS = {}
TOKENS = {}

async def generate_random_string(num: int):
    characters = string.ascii_letters + string.digits
    strng = ''.join(random.choice(characters) for _ in range(num))
    return strng

async def shrt_link(link, message):
    try:
        res = requests.get(f'https://{SHORTNER}/api?api={API}&url={quote(link)}')
        res.raise_for_status()
        data = res.json()
        slink = data.get('shortenedUrl')
        return slink

@vrfybot.on_message(filters.command('start'))
async def start(bot, message):
    user_id = message.from_user.id

    usr_cmd = message.text.split("_", 1)[-1]

    if usr_cmd == "/start":
        try:
            await message.reply("Hello, I am the verify bot")
        except Exception as e:
            print(f"Error replying to the message: {e}")

    elif usr_cmd.split("-", 1)[0] == "verify":
        parts = usr_cmd.split("-")
        if len(parts) == 3 and parts[0] == "verify":
            usr_token = parts[2]
            if user_id in VERIFIED_USERS:
                await bot.reply_text("You are already verified.")
            elif user_id in TOKENS and TOKENS[user_id] == usr_token:
                current_time = time.time()
                if current_time - VERIFIED[user_id]['timestamp'] < 24 * 60 * 60:
                    await bot.reply_text("You are verified for today.")
                    VERIFIED_USERS.append(user_id)
                else:
                    await bot.reply_text("Verification token has expired. Please try again later.")
            else:
                await bot.reply_text("Invalid verify token.")
        else:
            await bot.reply_text("Invalid verify link.")
    else:
        if user_id in VERIFIED_USERS:
            await bot.reply_text("You are already verified.")
        else:
            token = await generate_random_string(10)
            TOKENS[user_id] = token
            url = f"https://t.me/{bot.username}?start=verify-{user_id}-{token}"

            short_url = await shrt_link(url, message)

            if short_url:
                await bot.reply_text(f"Click on this link to verify: \n\n{short_url}")
            else:
                await bot.reply_text("Error in generating link, Please try again later.")

vrfybot.run()
