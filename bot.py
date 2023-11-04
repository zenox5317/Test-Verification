from os import getenv
from pyrogram import Client, filters
import random
import string
import time
import requests


API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
SHORTNER = getenv("SHORTNER", "")
API = getenv("API", "")

vrfybot = Client("vrfybot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, workers=500, in_memory=True)

VERIFIED = {}

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
            await message.reply("hello, I am verify bot")
        except Exception as e:
            print(f"Error replying to message: {e}")

  
    elif usr_cmd.split("-", 1)[0] == "verify":
        parts = usr_cmd.split("-")
        if len(parts) == 3 and parts[0] == "verify":
            usr_token = parts[2]
            if user_id in VERIFIED and VERIFIED[user_id]['token'] == usr_token:
                current_time = time.time()
                if current_time - VERIFIED[user_id]['timestamp'] < 24 * 60 * 60:
                    await bot.reply_text("You are Verified for today.")
                    VERIFIED.pop(user_id)
                else:
                    await bot.reply_text("verify token has expired. Please try again later.")
            else:
                await bot.reply_text("Invalid verify token.")
        else:
            await bot.reply_text ("Invalid verify link.")
     else:
         token = await generate_random_string(10)
         url = f"https://t.me/{bot.username}?start=verify-{user_id}-{verification_token}"

         short_url = await shrt_link(url)

         if short_url:
            await bot.reply_text(f"Click on this link to verify: {short_url}")
            VERIFIED[user_id] = {
                'token': usr_token,
                'timestamp': time.time()
            }
         else:
            await bot.reply_text("Error shortening the URL. Please try again later.")

verfybot.run()
