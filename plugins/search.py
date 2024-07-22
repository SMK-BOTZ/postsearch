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
    if f_sub == False:
        return
    
    channels = (await get_group(message.chat.id))["channels"]
    if not channels:
        return

    if message.text.startswith("/"):
        return

    query = message.text
    found = False  # Track if any message is found
    try:
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                await msg.forward(message.chat.id)
                found = True
                break  # Stop after forwarding the first matching message

        if not found:
            # If no results found, provide suggestions
            movies = await search_imdb(query)
            buttons = []
            for movie in movies:
                buttons.append([InlineKeyboardButton(movie['title'], callback_data=f"recheck_{movie['id']}")])

            await message.reply_photo(
                photo="https://graph.org/file/20f2a42c266a15b3118c8.jpg",
                caption="<b><I>I couldn't find anything related to your query 😕.\nDid you mean any of these?</I></b>",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@Client.on_callback_query(filters.regex(r"^recheck"))
async def recheck(bot, update):
    clicked = update.from_user.id
    try:
        typed = update.message.reply_to_message.from_user.id
    except:
        return await update.message.delete()

    if clicked != typed:
        return await update.answer("That's not for you! 👀", show_alert=True)

    await update.message.edit("Searching..💥")
    id = update.data.split("_")[-1]
    query = await search_imdb(id)
    channels = (await get_group(update.message.chat.id))["channels"]
    found = False

    try:
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                await msg.forward(update.message.chat.id)
                found = True
                break

        if not found:
            return await update.message.edit(
                "Still no results found! Please request to group admin",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 Request To Admin 🎯", callback_data=f"request_{id}")]])
            )
    except Exception as e:
        await update.message.edit(f"❌ Error: {e}")

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
    id = update.data.split("_")[1]
    name = await search_imdb(id)
    url = "https://www.imdb.com/title/tt" + id
    text = f"#RequestFromYourGroup\n\nName: {name}\nIMDb: {url}"
    await bot.send_message(chat_id=admin, text=text, disable_web_page_preview=True)
    await update.answer("✅ Request Sent To Admin", show_alert=True)
    await update.message.delete(60)
