from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, CallbackContext, PreCheckoutQueryHandler
import time
import logging
import os
import json
import random
import string
import requests
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By#tool to help in selection of elements withi our page
from selenium.webdriver.support.ui import WebDriverWait #wait unntil a particular element is visible on the page
from selenium.webdriver.support import expected_conditions as EC#desgin a conditio for your web drive to wait
from webdriver_manager.chrome   import ChromeDriverManager
from bs4 import BeautifulSoup
from user import BASE_URL, ADS_LINK, addFriend, refer
from product import create_product, update_product
from profiler import queryHandler, topup_balance, successful_payment
from group import updateGroup, addGroupMembers,createGroupPost
from friends import acceptFriendRequest
from post import createPost

#xTIC8lUd7N

TELEGRAM_TOKEN = "8446176836:AAGcPgTP9HRfp4g9qeoMnNIV2akVnjaa5WM"




#optional 
logging.basicConfig(
   # filename="telegram.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)


#required
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_id = update.message.chat.id

    BASEURL = "http://localhost:8000"
    userPhoto = user.get_profile_photos(limit=1)
    params = {
        "chat_id": chat_id,
        "from" : "Telegram",
        "first_name":user.first_name,
        "username"  : user.username,
        "last_name" : user.last_name,        
    }

    query_string =  urlencode(params, doseq=True, safe=":$")
    url = BASEURL + "?" + query_string

    response = requests.get(url=url)

    if ( response and response.data and response.data == "User not Exist" ) or not response:
         usered = {
                "chat_id": chat_id,
                "first_name" : user.first_name,
                "last_name" : user.last_name
            }

    
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Profile", callback_data="check-profile"), InlineKeyboardButton("Create Group", callback_data="create-group")],
        [InlineKeyboardButton("Product", callback_data="check-product"), InlineKeyboardButton("Create Adverts", callback_data="create-ads")],
        [InlineKeyboardButton(text="View Ads", url=ADS_LINK)]
    ])

    await update.message.reply_text(text=f"Hello {user.first_name}! You're welcome to Your Number One Social Bot. You can chat with any user by specifying the name or ID. \n Use /message [id] to start. \n Your chat ID is {chat_id}. Earn Points by refering friends to this group. Get Points by Specifying your referee - enter /referee [chat_id] to specify.", reply_markup=keyboard_markup)



async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    [id, *message]    = context.args
    current_user       = update.message.from_user
    message            = str( message )
    keyboard_markup     = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="View Ads", url=ADS_LINK)],       
    ])
    await context.bot.send_message(chat_id=id, text=f"Message From {current_user.first_name} \n {message} \n userid={id}", reply_markup=keyboard_markup)
    await update.message.reply_text("message sent!", reply_markup=keyboard_markup)



        
#used to start the application
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("message", message))
    application.add_handler(CommandHandler("createProduct", create_product))
    application.add_handler(CommandHandler("updateProduct", update_product))
    application.add_handler(CommandHandler("addGroupMembers", addGroupMembers))
    application.add_handler(CommandHandler("addFriend", addFriend))
    application.add_handler(CommandHandler("createGroupPost", createGroupPost))
    application.add_handler(CommandHandler("createPost", createPost))
    application.add_handler(CommandHandler("acceptRequest", acceptFriendRequest))
    application.add_handler(CommandHandler("updateGroup", updateGroup))
    application.add_handler(CommandHandler("referee", refer))
    application.add_handler(CallbackQueryHandler(queryHandler))
    application.add_handler(CallbackQueryHandler(topup_balance))
    application.add_handler(MessageHandler(filters=filters.SUCCESSFUL_PAYMENT, callback=successful_payment))
    print("Application Running")
    application.run_polling()
    #will not run


if __name__  == "__main__" :
    main()

# Use Firefox instead of Chrome
