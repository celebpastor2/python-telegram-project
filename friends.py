from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from telegram.ext import ContextTypes
from user import BASE_URL, ADS_LINK
import json
        
async def acceptFriendRequest(update:Update, context: ContextTypes.DEFAULT_TYPE ):
    try:
        [id] = context.args
        user = update.message.from_user
        chat_id = update.message.chat.id
        
        """endpoint = "/accept-telegram-friend/"
        data = {
            "friend_id" : id,
            "chat_id"   : chat_id
        }

        response = requests.post(f"{BASE_URL}{endpoint}", data=data)

        await update.message.reply_text(response.text)
        await context.bot.send_message(chat_id=id, text=f"Friend Request From {user.first_name} \n accept by running /acceptRequest {chat_id}")"""
        await update.message.reply_text("Friend Request  Accepted")

    except Exception as e:
        keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Accept Friend Request", callback_data=f"add-friend-{chat_id}")], [InlineKeyboardButton("View Ads", url=ADS_LINK)]])
        await update.message.reply_text("Error Send Request \n Ensure your request was formatted like this \n /friend [id] ", reply_markup=keyboard_markup)
