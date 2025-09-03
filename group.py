from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from telegram.ext import ContextTypes
from user import BASE_URL, ADS_LINK
import json


async def addGroupMembers(update: Update, context: ContextTypes.DEFAULT_TYPE ):
    try :
        [group_id, member_id] = context.args
        endpoint = "/update-user-group/"

        data = {
            "group_id"  : group_id,
            "chat_id"   : member_id
        }
        response = requests.post(f"{BASE_URL}{endpoint}", data=data)

        await update.message.reply_text(response.text)        

    except :
        await update.message.reply_text("Please ensure you are using the required format to run this command \n format required is the following \n /addGroupMembers [group_id] [member_chat_id]")

async def updateGroup(update: Update, context: ContextTypes.DEFAULT_TYPE ):
    try :
        [group_id, group_name, *description] = context.args
        endpoint = "/update-user-group/"

        data = {
            "group_id"  : group_id,
            "group_name"   : group_name,
            "description"   : description
        }
        response = requests.post(f"{BASE_URL}{endpoint}", data=data)

        await update.message.reply_text(response.text)        

    except :
        await update.message.reply_text("Please ensure you are using the required format to run this command \n format required is the following \n /updateGroup [group_id] [group_name][description]")


        
async def createGroupPost(update:Update, context: ContextTypes.DEFAULT_TYPE ):
    try:
        [group_id, *content] = context.args
        user = update.message.from_user
        chat_id = update.message.chat.id
        
        endpoint = "/create-post/"
        data = {
            "chat_id"   : chat_id,
            "content"   : content,
            "context"   : "group",
            "group_id"  : group_id
        }

        response = requests.post(f"{BASE_URL}{endpoint}", data=data)

        await update.message.reply_text(response.text)

        endpoint = "/get-group-memebers/"
        data = {
            "group_id"   : group_id
        }

        response = requests.post(f"{BASE_URL}{endpoint}", data=data)

        try :

            friends = json.loads(response.text)

            for friend in friends :
                chat_id = friend.chat_id
                await context.bot.send_message(chat_id=chat_id, text=f"Post from  {user.first_name} \n {content} \n {chat_id}")

        except :
            await update.message.reply_text("Couldn't update Group Memebrs")


    except Exception as e:
        keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Accept Friend Request", callback_data=f"add-friend-{chat_id}")], [InlineKeyboardButton("View Ads", url=ADS_LINK)]])
        await update.message.reply_text("Error Send Request \n Ensure your request was formatted like this \n /friend [id] ", reply_markup=keyboard_markup)
