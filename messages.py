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

#xTIC8lUd7N

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

async def create_product(update: Update, context: ContextTypes.DEFAULT_TYPE ) :
    try :
        [name, price, image_url, stock, *description] = context.args
        endpoint = "/create-product/"
        data = {
            'name'  : name,
            'price'   : price,
            'image'    : image_url,
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
        endpoint = "/update-product/"
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


async def queryHandler(update: Update, context:CallbackContext ):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    chat_id = update.effective_chat.id

    print(f" Query Data {query.data}")


    if query.data == "create-group" :
        letters = string.ascii_letters + string.digits
        group_id = ""
        for _ in range(10) :
            group_id += str( random.choice(letters) )
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
        endpoint = "/create-user-group/"
        data = {
            'group_id'  : group_id,
            'chat_id'   : chat_id,

        }
        response =  requests.post(BASE_URL + endpoint, data=data, headers={'Content-Type' : 'application/json'})
        if not response.text == "Group Creator Does not Exists":
            await query.edit_message_text(f"Group Successfully Created with ID: \n {group_id} \n update group with /updateGroup {group_id} [group_name] [description] \n add members to group using /addGroupMembers {group_id} [member_chat_id]")

        else :
            await query.edit_message_text(f"Group Not Successfully Created")

    elif query.data == "check-profile" :
        endpoint = f"/get-telegram-user?chat_id={chat_id}"
        response = requests.get(f"{BASE_URL}{endpoint}")
        first_name = user.first_name
        last_name = user.last_name
        phone_number = "/set_phone [phone_number]"
        username    = user.username
        location   = "/set_location [location]"
        balance   = 0.0
        print("profile result ", response.text.lower())
        if not response.text.lower() == "no user found" :
            response = json.loads(response.text)
            first_name = response['first_name'] or user.first_name
            last_name = response['last_name'] or user.last_name
            username = response['username'] or user.username
            location = response['location'] or "/set_location [location]"
            phone_number = response['phone_number'] or "/set_phone [phone_number]"
            balance = response['balance']

        
        keyboard_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="View Friends", callback_data="viewfriends"),InlineKeyboardButton(text="Make Friends", callback_data="makefriends")],      
            ])

        await query.edit_message_text(f"First Name: {first_name}" f" \n Last Name: {last_name}" f" \n Phone number: {phone_number}" f" \n Username: {username}" f" \n Location: {location}" f" \n Balance: {balance}" , reply_markup=keyboard_markup)

    elif query.data.lower() == "viewfriends" :
        print("viewing friends...")
        endpoint = f"/get-telegram-friends/"
        data = {
            "chat_id"   : chat_id
        }
        response = requests.post(f"{BASE_URL}{endpoint}", data=data)
        print("response from friends server: ", response.text )
        keyboard_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="View Profile", callback_data="check-profile"),InlineKeyboardButton(text="Make Friends", callback_data="makefriends")],      
            ])
        if response.text :
            friends = json.loads(response.text)
            resp_text = f"Total Friends Found {len(friends)}"

            for friend in friends :
                resp_text += f"\n {friend['name']} {friend[chat_id]}"
            
            resp_text  = f"\n chat with any friend using /message [friend_id] [message...]"
            await query.edit_message_text(resp_text, reply_markup=keyboard_markup)

        else :
            await query.edit_message_text("No friends found", reply_markup=keyboard_markup)

        return
    elif query.data == "makefriends" :
        endpoint = "/get-telegram-users/"
        response = requests.get(f"{BASE_URL}{endpoint}")
        print("response for all users ", response.text )
        if response.text :
            users = list( json.loads(response.text) )
            random.shuffle(users)
            print(type(users))
            if len(users) > 15 :
                users = users[:15]

            text  = ""
            for user in users :
                text += f"username - {user['username']} chat ID - {user['chat_id']} \n"

            text += "run /addFriend [friend_id] to add any friend from the list"

            await query.edit_message_text(text)
        else :
            await query.edit_message_text("User not found")
        return
    elif query.data == "check-product" :
        endpoint    = "/get-products"
        try :
            response = requests.get(f"{BASE_URL}{endpoint}")
            products = json.loads(response.text)
            text     = ""
            print(f"Response Gotten {response.text}")

            for product in products:
                text += f"id - {product._id} name - {product.name} price - ${product.price} \n\n"

            if not text :
                text += "No Product Available Yet \n\n You can be the first to add product using the following Command \n\n /createProduct [product_name] [product_price] [image_url] [stock] [description]"

            keyboard_markup   = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Previous", callback_data="product-prev-0"), InlineKeyboardButton(text="Next", callback_data="product-next-2")],      
                [InlineKeyboardButton(text="Create Product", callback_data="create-product")],      
            ])

            await query.edit_message_text(text, reply_markup=keyboard_markup)

        except Exception as e:
            print(f"error fetching product {e}")
            await query.edit_message_text("Oops Couldn't fetch products")

    elif "product-next" in query.data or "product-prev" in query.data:
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
        
        endpoint = "/add-telegram-friend/"
        data = {
            "friend_id" : id,
            "chat_id"   : chat_id
        }

        response = requests.post(f"{BASE_URL}{endpoint}", data=data)

        await update.message.reply_text(response.text)
        await context.bot.send_message(chat_id=id, text=f"Friend Request From {user.first_name} \n accept by running /acceptRequest {chat_id}")


    except Exception as e:
        keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Accept Friend Request", callback_data=f"add-friend-{chat_id}")], [InlineKeyboardButton("View Ads", url=ADS_LINK)]])
        await update.message.reply_text("Error Send Request \n Ensure your request was formatted like this \n /friend [id] ", reply_markup=keyboard_markup)


async def createPost(update:Update, context: ContextTypes.DEFAULT_TYPE ):
    try:
        [*content] = context.args
        user = update.message.from_user
        chat_id = update.message.chat.id
        
        endpoint = "/create-post/"
        data = {
            "chat_id"   : chat_id,
            "content"   : content
        }

        response = requests.post(f"{BASE_URL}{endpoint}", data=data)

        await update.message.reply_text(response.text)

        endpoint = "/get-telegram-friends/"
        data = {
            "chat_id"   : chat_id
        }

        response = requests.post(f"{BASE_URL}{endpoint}", data=data)

        try :

            friends = json.loads(response.text)

            for friend in friends :
                chat_id = friend.chat_id
                await context.bot.send_message(chat_id=chat_id, text=f"Post from  {user.first_name} \n {content} \n {chat_id}")

        except :
            await update.message.reply_text("Couldn't update friends")


    except Exception as e:
        keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Accept Friend Request", callback_data=f"add-friend-{chat_id}")], [InlineKeyboardButton("View Ads", url=ADS_LINK)]])
        await update.message.reply_text("Error Send Request \n Ensure your request was formatted like this \n /friend [id] ", reply_markup=keyboard_markup)
        
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



        
#used to start the application
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("message", message))
    application.add_handler(CommandHandler("createProduct", create_product))
    application.add_handler(CommandHandler("updateProduct", update_product))
    application.add_handler(CommandHandler("addGroupMembers", addGroupMembers))
    application.add_handler(CommandHandler("addFriend", addFriend))
    application.add_handler(CommandHandler("acceptRequest", acceptFriendRequest))
    application.add_handler(CommandHandler("updateGroup", updateGroup))
    application.add_handler(CommandHandler("referee", refer))
    application.add_handler(CallbackQueryHandler(queryHandler))
    print("Application Running")
    application.run_polling()
    #will not run


if __name__  == "__main__" :
    main()

# Use Firefox instead of Chrome
