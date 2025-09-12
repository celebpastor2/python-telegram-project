from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from telegram.ext import ContextTypes
import json

BASE_URL    = "http://localhost:8000"
ADS_LINK    = "https://www.profitableratecpm.com/armxiuwyu?key=1da115d4d39828e534c0206c4af9f885"
CLIENT_ID   = "1275654567290162"
PROVIDER_TOKEN = ""


async def addFriend(update:Update, context: ContextTypes.DEFAULT_TYPE ):
    try:
        [id] = context.args
        user = update.message.from_user
        chat_id = update.message.chat.id
        
        endpoint = "/add-telegram-friend/"

        if chat_id == id :
            await update.message.reply_text("Can't send friend request to yourself")
            return
        
        data = {
            "friend_id" : id,
            "chat_id"   : chat_id
        }

        response = requests.post(f"{BASE_URL}{endpoint}", data=data)
        text = response.text
        print(text)
        await update.message.reply_text(text[:100])
        await context.bot.send_message(chat_id=id, text=f"Friend Request From {user.first_name} \n accept by running /acceptRequest {chat_id}")


    except Exception as e:
        print(e)
        keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Accept Friend Request", callback_data=f"add-friend-{chat_id}")], [InlineKeyboardButton("View Ads", url=ADS_LINK)]])
        await update.message.reply_text("Error Send Request \n Ensure your request was formatted like this \n /friend [id] ", reply_markup=keyboard_markup)



async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE ):
    chat_id = update.message.chat.id
    try :
        [referee] = context.args
        endpoint = f"/get-telegram-user?chat_id={referee}"
        response = requests.get(f"{BASE_URL}{endpoint}")

        if response.text and response.text.lower() == "no user found" :
            await update.message.reply_text("Invalid Referee Selected...Check Your Referee ID and Try again")

        else :
            endpoint = f"/add-referee?chat_id={referee}"
            requests.get(f"{BASE_URL}{endpoint}")
            endpoint =  "/add-balance"
            userAdd = 100
            refereeAdd = 250
            endpoint += f"?chat_id={chat_id}&balance={userAdd}"
            requests.get(f"{BASE_URL}{endpoint}")
            endpoint =  f"/add-balance?chat_id={referee}&balance={refereeAdd}"
            requests.get(f"{BASE_URL}{endpoint}")
            await update.message.reply_text("Sucessfully added referee to your account. Your account has been successfully credited with 100 points")   
    except :
        await update.message.reply_text("Enter your referal ID. Use this format \n\n /referee [referal_id]")
