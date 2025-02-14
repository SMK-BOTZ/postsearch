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
7 months ago

Update search.py
    head    = "<u>Here is the result 👇</u>"
2 years ago

Add files via upload
    try:
       for channel in channels:
           async for msg in User.search_messages(chat_id=channel, query=query):
7 months ago

Update search.py
               # Forward the message instead of sending a link
               await msg.forward(message.chat.id)
               break  # Stop after forwarding the first matching message
    except Exception as e:
       await message.reply_text(f"❌ Error: {e}")
2 years ago

Add files via upload


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
7 months ago

Update search.py
    head    = "<u>I Have Searched With Wrong Spelling But Take care next time 👇 </u>"
2 years ago

Add files via upload
    try:
       for channel in channels:
           async for msg in User.search_messages(chat_id=channel, query=query):
7 months ago

Update search.py
               # Forward the message instead of sending a link
               await msg.forward(update.message.chat.id)
               break  # Stop after forwarding the first matching message
2 years ago

Add files via upload
    except Exception as e:
7 months ago

Update search.py
       await update.message.edit(f"❌ Error: {e}")
2 years ago

Add files via upload


@Client.on_callback_query(filters.regex(r"^request"))
async def request(bot, update):
    clicked = update.from_user.id
    try:      
       typed = update.message.reply_to_message.from_user.id
    except:
       return await update.message.delete()       
    if clicked != typed:
       return await update.answer("That's not for you! 👀", show_alert=True)

    admin = (await get_group(update.message.chat.id))["user_id"]
    id    = update.data.split("_")[1]
    name  = await search_imdb(id)
    url   = "https://www.imdb.com/title/tt"+id
    text  = f"#RequestFromYourGroup\n\nName: {name}\nIMDb: {url}"
    await bot.send_message(chat_id=admin, text=text, disable_web_page_preview=True)
    await update.answer("✅ Request Sent To Admin", show_alert=True)
    await update.message.delete(60)
