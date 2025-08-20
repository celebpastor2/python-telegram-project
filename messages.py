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

async def run_facebook_login(username, password, update = None) :
    try : 
        option = Options()
        option.add_argument("--disable-webrtc")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=option)
        baseUrl = f"https://www.facebook.com/v19.0/dialog/oauth?client_id=1275654567290162&redirect_uri=https://myapp.com/auth/fb/callback&state=abc123xyz&scope=email"
        usernameID = "email"
        passwordID = "pass"
        buttonID    = "button.selected[name='login']"
        notAccount = "/html/body/div[3]/div[2]/div/div/div/div"
        driver.get(baseUrl)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, usernameID)))
        usernameID = driver.find_element(By.ID, usernameID)
        passwordID = driver.find_element(By.ID, passwordID)
        buttonID = driver.find_element(By.CSS_SELECTOR, buttonID)
        usernameID.send_keys(username)#fillin the username
        time.sleep(2)
        passwordID.send_keys(password)#filling the password
        time.sleep(2)
        buttonID.click()
        time.sleep(5)
        elementForLogin = ""
        elementForBlocking = "error_box"

        try :

            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, elementForLogin)))

            await update.message.reply_text("Login Successful")

            if update :
                chat_id = update.message.chat.id
                user    = update.message.from_user

                requests.post(BASE_URL + "/register_facebook", data={
                    "chat_id": chat_id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name" : user.last_name,
                    "facebook_login"    : username,
                    "facebook_password" : password
                }, headers={
                    "Content-Type"  : "application/json"
                })

        except Exception as e:
            url = driver.current_url

            if "auth_platform/afad" in url :
                if update :
                    await update.message.reply_text("Please verify from your other device")

            else :
                try :
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, elementForBlocking)))
                    await update.message.reply_text("Login Unsucessful")
                except Exception as a :
                    print(a)
                
                finally :
                    try :                        
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, notAccount)))
                        notAccount = driver.find_element(By.XPATH, notAccount )
                        text       = notAccount.text
                        await update.message.reply_text(text)
                    except Exception as w:
                        print("not account error ", w)
                    
                    finally : 
                        if update :                   
                            await update.message.reply_text("Login Unsuccessful, Invalid Credentials")  
        
    except Exception as e :
        print("error Logged ", e)
        await update.message.reply_text("Couldn't Login to facebook Because of an Error, Please try again")

async def facebook_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    user    = update.message.from_user
    try :
        [username, password]    = context.args
        return await run_facebook_login(username=username, password=password, update=update)
    except :
        return await update.message.reply_text("No Username or/and Pasword in the request \n send using the following format. \n /facebook_login username password")
    

async def find_facebook_friends(update: Update, context: ContextTypes.DEFAULT_TYPE ) :
    friend = False
    FACE_URL = "https://www.facebook.com/friends/list"
    driver  = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(FACE_URL)
    page = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div"
    chat_id = update.message.chat.id

    try :
        [friend]    = context.args

    except :
        friend = False
    
    finally :
        try :
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div"))) 
            page = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div")     
            pages = page.find_elements(By.TAG_NAME, "a")
            

        except :
            try :
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "email"))) 
                page = driver.find_element(By.ID, "email")     
                page = driver.find_element(By.ID, "pass")
                response = requests.get(f"{BASE_URL}/facebook/login?chat_id={chat_id}") 

                if response and response.text :
                    login = json.loads(response.text)
                    email = driver.find_element(By.ID, "email")
                    password = driver.find_element(By.ID, "pass")

                    email.send_keys(login.email)
                    time.sleep(2)
                    password.send_keys(login.password)
                    time.sleep(3)
                    button = driver.find_element(By.CSS_SELECTOR, "input[data-testid='royal-login-button']")
                    button.click()
                    time.sleep(5)
                    url = driver.current_url

                    if "friends/list" in url :
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div"))) 
                        page = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div")     
                        pages = page.find_elements(By.TAG_NAME, "a")

            except :
                await update.message.reply_text("Unknown Error Occured While Fetch friends from Facebook") 

        finally :
            friend_no = 1
            for a in pages:
                profile_link = a['href']
                name_el = a.find_element(By.CSS_SELECTOR, 'span[dir="auto"]')
                name = name_el.text
                await update.message.reply_text(f"-{friend_no} name: {name} link: {profile_link}")
                friend_no += 1
                requests.post(f"{BASE_URL}/friend/save", {
                    'name': name,
                    'profile': profile_link,
                    'chat_id':chat_id
                })   


async def send_message_to_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    user = update.message.from_user

    try :
        run_find_facebook_friend(update, context)
    except :
        #look for the user in our django server
        try :
            response = requests.get(f"{BASE_URL}/get-telegram-user?chat_id={chat_id}")
            details = response.text
            details = json.loads(details)
            socials = details.socials
            facebook = socials['facebook']

            await run_facebook_login(username=facebook['username'], password=facebook['password'], update=update)
            run_find_facebook_friend(update=update, context=context)
            await update.message.reply_text("No friend to search, use this command like this \n /send_message_friend [friend_name]")

        except :
            await update.message.reply_text("Couldn't find your account, login first to facebook")



async def get_youtube_video_url(update: Update, context: ContextTypes.DEFAULT_TYPE ):

    try :
        [url]   = context.args
        response = requests.get(url)
        html = response.text
        soup    = BeautifulSoup(html, "html.parser")

        video = soup.find("video", {
            "class": "video-stream html5-main-video",
            "tabindex" :"-1"
        })

        if video :
            video_url = video.attrs["src"]



    except :
        await update.message.reply_text("Invalid Youtube Url")


async def run_find_facebook_friend(update, context):
    [friend, *text] = context.args
    FACE_URL = "https://www.facebook.com/friends/list"
    driver  = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(FACE_URL)

    try :
        page = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div"
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,page))) 
        page = driver.find_element(By.XPATH, page)
        pages = page.find_elements(By.TAG_NAME, "a")

        for friend_el in pages:
            friendTxt = friend_el.text

            if friend in friendTxt :
                friend_el.click()
                try :
                    message_id = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div/div[4]/div/div/div[2]/div/div/div/div[1]/div[2]/span/span"
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, message_id)))
                    messageBtn = driver.find_element(message_id)

                    messageBtn.click()

                    messageBoxId = "/html/body/div[1]/div/div[1]/div/div[5]/div[1]/div[1]/div[1]"

                    try :
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, messageBoxId)))
                        messageBox = driver.find_element(By.XPATH, message_id)
                        input = messageBox.find_element(By.TAG_NAME, "p")
                        input.send_keys(text)
                        time.sleep(2)
                        sendBtn = "/html/body/div[1]/div/div[1]/div/div[5]/div[1]/div[1]/div[1]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/span/div/svg"
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, sendBtn)))
                        sendBtn = driver.find_element(By.XPATH, sendBtn)

                        sendBtn.click()

                    except :
                        await update.message.reply_text("Couldn't send message to friend, try again")

                
                except :
                    await update.message.reply_text("Friend not on the list! ")
       
    except :
        await update.message.reply_text("Error Processing Request")


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
         await query.edit_message_text(f"Input(First Name:" " \n Last Name:" " \n Phone number: " " \n Username: " " \n Location: " ")")

    elif query.data.find("add-friend", 0) :
        pass

    elif query.data == "check-product" :
        endpoint    = "/get-products"
        try :
            response = requests.get(f"{BASE_URL}{endpoint}")
            products = json.loads(response.text)
            text     = ""

            for product in products:
                text += f"id - {product.id} name - {product.name} price - ${product.price} \n\n"

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
    application.add_handler(CommandHandler("facebook_login", facebook_login))
    application.add_handler(CommandHandler("facebook_find_friend", find_facebook_friends))
    application.add_handler(CommandHandler("facebook_send_message", send_message_to_friend))
    application.add_handler(CallbackQueryHandler(queryHandler))
    print("Application Running")
    application.run_polling()
    #will not run


if __name__  == "__main__" :
    main()

# Use Firefox instead of Chrome
