from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from telegram.ext import ContextTypes
from user import BASE_URL, ADS_LINK
import json



async def createPost(update:Update, context: ContextTypes.DEFAULT_TYPE ):
    try:
        [*content] = context.args
        user = update.message.from_user
        chat_id = update.message.chat.id
        content = " ".join(content)
        
        endpoint = "/create-post/"
        data = {
            "chat_id"   : chat_id,
            "content"   : content
        }
        

        response = requests.post(f"{BASE_URL}{endpoint}", data=data)
       

        await update.message.reply_text(response.text  + "\n\n" + content)
        
        endpoint = "/get-telegram-friends/"
        data = {
            "chat_id"   : chat_id
        }

        response = requests.post(f"{BASE_URL}{endpoint}", data=data)

        try :

            friends = json.loads(response.text)

            for friend in friends :
                friend_id = friend['chat_id']
                await context.bot.send_message(chat_id=friend_id, text=f"Post from  {user.first_name} \n {content} \n {chat_id}")

        except Exception as e :
            print(e)
            await update.message.reply_text("Couldn't update friends")


    except Exception as e:
        print(e)
        keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Accept Friend Request", callback_data=f"add-friend-{chat_id}")], [InlineKeyboardButton("View Ads", url=ADS_LINK)]])
        await update.message.reply_text("Error Send Request \n Ensure your request was formatted like this \n /createPost [content...] all the content you want to write", reply_markup=keyboard_markup)

async def Sharepost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        [*content] = context.args
        user = update.message.from_user
        chat_id = update.message.chat.id

        endpoint = "/share-post/"

        payload = {
            "user": user,
            "chat_id": chat_id,
            "text": content
        }

        response = requests.post(f"{BASE_URL}{endpoint}", payload=payload)

        return response.json()
    
    except Exception as e :
        await update.message.reply_text("You can't share post")


