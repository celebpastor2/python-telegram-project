from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, CallbackContext
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

TELEGRAM_TOKEN = "7936586039:AAFBxzXW78tq9OArvZm5BfQiBPM3Kuta0C0"
ADS_LINK    = "https://www.profitableratecpm.com/armxiuwyu?key=1da115d4d39828e534c0206c4af9f885"
BASE_URL    = "http://localhost:8000"
CLIENT_ID   = "1275654567290162"



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
    params = {
        "chat_id": chat_id,
        "from" : "Telegram"
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

    await update.message.reply_text(text=f"Hello {user.first_name}! You're welcome to Your Number One Social Bot. You can chat with any user by specifying the name or ID. \n Use /message [id] to start. \n Your chat ID is {chat_id}", reply_markup=keyboard_markup)



async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    [id, *message]    = context.args
    current_user       = update.message.from_user
    message            = str( message )
    keyboard_markup     = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="View Ads", url=ADS_LINK)],       
    ])
    await context.bot.send_message(chat_id=id, text=f"Message From {current_user.first_name} \n {message} \n userid={id}", reply_markup=keyboard_markup)
    await update.message.reply_text("message sent!", reply_markup=keyboard_markup)

async def create_product(update: Update, context: ContextTypes.DEFAULT_TYPE ) :
    try :
        [name, price, stock, *description] = context.args
        endpoint = "/create-product"
        data = {
            'name'  : name,
            'price'   : price,
            'stock' : stock,
            'description' : description
        }
        response =  requests.post(BASE_URL + endpoint, data=data, headers={'Content-Type' : 'application/json'})
        await update.message.reply_text(response.text)
    except :
        await update.message.reply_text("No name or price or stock or description argument in the request. \n\n \t Request should be formated as follows: \n\n\t /create_product [name] [price] [stock] [description]")

async def update_product(update: Update, context: ContextTypes.DEFAULT_TYPE ) :
    try :
        [name, price, stock, *description] = context.args
        endpoint = "/update-product"
        data = {
            'name'  : name,
            'price'   : price,
            'stock' : stock,
            'description' : description
        }
        response =  requests.post(BASE_URL + endpoint, data=data, headers={'Content-Type' : 'application/json'})
        await update.message.reply_text(response.text)
    except :
        await update.message.reply_text("No name or price or stock or description argument in the request. \n\n \t Request should be formated as follows: \n\n\t /update_product [name] [price] [stock] [description]")

async def queryHandler(update: Update, context:CallbackContext ):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    chat_id = update.effective_chat.id


    if query.data == "create-group" :
        group_id = string.ascii_letters + string.digits
        group_id = ""
        for _ in range(10) :
            group_id += str( random.choice(group_id) )
            """directory = os.path.join(os.getcwd(), "groups")
            filename  = os.path.join(directory, f"{group_id}-{chat_id}.json")

            with open(filename) as file:
                group_members = []
                usered = {
                    "id":chat_id,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "code":user.language_code,

                }
                group_members.append(usered)
                file.write(json.dumps( group_members ))"""
        endpoint = "create-user-group"
        data = {
            'group_id'  : group_id,
            'chat_id'   : chat_id,

        }
        response =  requests.post(BASE_URL + endpoint, data=data, headers={'Content-Type' : 'application/json'})
        if response.text == "":
            await query.edit_message_text(f"Group Successfully Created with ID: \n {group_id}")

        else :
            await query.edit_message_text(f"Group Not Successfully Created")

    elif query.data == "check-profile" :
         
         await query.edit_message_text(f"First Name: " " \n Last Name:" " \n Phone number: " " \n Username: " " \n Location: " )

    elif query.data.find("add-friend", 0) :
        pass

    elif query.data == "check-product" :
        endpoint    = "/get-products"
        try :
            response = requests.get(f"{BASE_URL}{endpoint}")
            products = json.loads(response.text)
            text     = ""

            for product in products:
                text += f"id - {product._id} name - {product.name} price - ${product.price} \n\n"

            keyboard_markup   = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Previous", callback_data="product-prev-0"), InlineKeyboardButton(text="Next", callback_data="product-next-2")],      
                [InlineKeyboardButton(text="Create Product", callback_data="create-product")],      
            ])

            await query.edit_message_text(text, reply_markup=keyboard_markup)

        except :
            await query.edit_message_text("Oops Couldn't fetch products")

    elif query.data.find("product-next", 0) or query.data.find("product-prev", 0):
        page        = query.data.split("-")[2]
        endpoint    = f"/get-products?page={page}"
        try :
            response = requests.get(f"{BASE_URL}{endpoint}")
            products = json.loads(response.text)
            text     = ""

            for product in products:
                text += f"id - {product.id} name - {product.name} price - ${product.price} \n\n"

            keyboard_markup   = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Previous", callback_data=f"product-prev-{page-1}"), InlineKeyboardButton(text="Next", callback_data=f"product-next-{page+1}")],      
                [InlineKeyboardButton(text="Create Product", callback_data="create-product")],      
            ])

            await query.edit_message_text(text, reply_markup=keyboard_markup)

        except :
            await query.edit_message_text("Oops Couldn't fetch products")

    elif query.data == "create-product" :
        await query.edit_message_text("create product by entering these command \n /create_product [product-name] [price] ")


   


async def addFriend(update:Update, context: ContextTypes.DEFAULT_TYPE ):
    try:
        [id] = context.args
        user = update.message.from_user
        chat_id = update.message.chat.id
        
        directory = os.path.join(os.getcwd(), "users")
        filename  = os.path.join(directory, f"{id}.json")

        if os.path.exists(filename) :
            keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Accept Friend Request", callback_data=f"add-friend-{chat_id}")], [InlineKeyboardButton("View Ads", url=ADS_LINK)]])
            await context.bot.send_message(id, f"Hello \n {user.first_name} wants to be your friend", reply_markup=keyboard_markup)

        else :
            keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Accept Friend Request", callback_data=f"add-friend-{chat_id}")], [InlineKeyboardButton("View Ads", url=ADS_LINK)]])
            await update.message.reply_text("User Does Not Exist", reply_markup=keyboard_markup)


    except Exception as e:
        keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Accept Friend Request", callback_data=f"add-friend-{chat_id}")], [InlineKeyboardButton("View Ads", url=ADS_LINK)]])
        await update.message.reply_text("Error Send Request \n Ensure your request was formatted like this \n /friend [id] ", reply_markup=keyboard_markup)

        

        
    
    
 


#used to start the application
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("message", message))
    application.add_handler(CommandHandler("createProduct", create_product))
    application.add_handler(CommandHandler("updateProduct", update_product))
    application.add_handler(CallbackQueryHandler(queryHandler))
    print("Application Running")
    application.run_polling()
    #will not run


if __name__  == "__main__" :
    main()

# Use Firefox instead of Chrome
