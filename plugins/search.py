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

@Client.on_callback_query(filters.regex(r"^recheck"))
async def recheck(bot, update):
    clicked = update.from_user.id
    try:      
       typed = update.message.reply_to_message.from_user.id
    except:
       return await update.message.delete(2)       
    if clicked != typed:
       return await update.answer("That's not for you! 👀", show_alert=True)

    m=await update.message.edit("Searching..💥")
    id      = update.data.split("_")[-1]
    query   = await search_imdb(id)
    channels = (await get_group(update.message.chat.id))["channels"]
    head    = "<u>I Have Searched With Wrong Spelling But Take care next time 👇 </u>"
    try:
       for channel in channels:
           async for msg in User.search_messages(chat_id=channel, query=query):
               # Forward the message instead of sending a link
               await msg.forward(update.message.chat.id)
               break  # Stop after forwarding the first matching message
    except :
        pass

