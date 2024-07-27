import asyncio
from info import *
from utils import *
from time import time
from client import User
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Set a limit on the number of messages to forward at once
FORWARD_LIMIT = 1

@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    f_sub = await force_sub(bot, message)
    if f_sub == False:
        return
    
    channels = (await get_group(message.chat.id))["channels"]
    if not channels:
        return

    if message.text.startswith("/"):
        return

    query = message.text
    forward_count = 0  # Counter to limit the number of forwards

    try:
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                if forward_count < FORWARD_LIMIT:  # Check the limit before forwarding
                    await msg.forward(message.chat.id)
                    forward_count += 1
                else:
                   pass
       
