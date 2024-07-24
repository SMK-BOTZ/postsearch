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
    head    = "<u>Here is the results 👇\n\n👇</u> <b><I>👇</I></b>\n\n"
    results = ""
    try:
       for channel in channels:
           async for msg in User.search_messages(chat_id=channel, query=query):
               name = (msg.text or msg.caption).split("\n")[0]
               if name in results:
                  continue 
               results += f"<b><I>👉 {name}\n🔗 {msg.link}</I></b>\n\n"                                                      
       if bool(results)==False:
          movies = await search_imdb(query)
          buttons = []
          for movie in movies: 
              buttons.append([InlineKeyboardButton(movie['title'], callback_data=f"recheck_{movie['id']}")])
          msg = await message.reply_photo(photo="https://telegra.ph/file/cf6706158b0bfaf436f54.jpg",
                                          caption="<b><I>I Couldn't find anything related to Your Query😕.\nDid you mean any of these?</I></b>", 
                                          reply_markup=InlineKeyboardMarkup(buttons))
       else:
          msg = await message.reply_text(text=head+results, disable_web_page_preview=True)
       _time = (int(time()) + (15*60))
       await save_dlt_message(msg, _time)
    except:
       pass
       


