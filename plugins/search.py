import asyncio
from info import *
from utils import *
from time import time
from client import User
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    f_sub = await force_sub(bot, message)
    if f_sub==False:
       return     
    channels = (await get_group(message.chat.id))["channels"]
    if bool(channels)==False:
       return     
    if message.text.startswith("/"):
       return    
    query   = message.text
    try:
       for channel in channels:
           async for msg in User.search_messages(chat_id=channel, query=query):
               # Forward the message instead of sending a link
               await msg.forward(message.chat.id)
               break  # Stop after forwarding the first matching message
    except :
       pass
