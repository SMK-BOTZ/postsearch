import asyncio
from info import *
from utils import *
from client import User
from pyrogram import Client, filters

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

    query = message.text.strip().lower()  # Convert the query to lowercase for case-insensitive comparison
    links = []  # List to store message links

    try:
        for channel in channels:
            try:
                async for msg in User.search_messages(chat_id=channel, query=query):
                    # Check for exact match
                    message_text = (msg.text or msg.caption).strip().lower()  # Ensure text is lowercase and stripped
                    if query == message_text:
                        # Append message link to the list
                        links.append(msg.link)
            except Exception as e:
                print(f"Error accessing channel {channel}: {e}")

        # Send the links to the group if any are found
        if links:
            response = "\n".join(links)
            await message.reply_text(response, disable_web_page_preview=True)
    except Exception as e:
        print(f"❌ Error: {e}")
