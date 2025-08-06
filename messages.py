from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, CallbackContext
import time
import logging
import os
import json
import random
import string
import requests

TELEGRAM_TOKEN = "7936586039:AAFBxzXW78tq9OArvZm5BfQiBPM3Kuta0C0"
ADS_LINK    = "https://www.profitableratecpm.com/armxiuwyu?key=1da115d4d39828e534c0206c4af9f885"



#optional 
logging.basicConfig(
    filename="telegram.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)


#required
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_id = update.message.chat.id
    directory = os.path.join(os.getcwd(), "users")
    filename  = os.path.join(directory, f"{chat_id}.json")
    with open(filename, "w+") as file :
        usered = {
            "chat_id": chat_id,
            "first_name" : user.first_name,
            "last_name" : user.last_name
        }
        file.write(json.dumps(usered))

    
    keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Profile", callback_data="check-profile"), InlineKeyboardButton("Create Group", callback_data="create-group")],
        [InlineKeyboardButton(text="View Ads", url=ADS_LINK)]
    ])

    await update.message.reply_text(text=f"Hello {user.first_name}! You're welcome to your chat bot. You can chat with any user by specifying the name or ID. \n Use /message [id] to start. \n Your chat ID is {chat_id}", reply_markup=keyboard_markup)



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
            directory = os.path.join(os.getcwd(), "groups")
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
                file.write(json.dumps( group_members ))

    elif query.data == "check-profile" :
         await query.edit_message_text(f"Input(First Name:" " \n Last Name:" " \n Phone number: " " \n Username: " " \n Location: " ")")

    elif query.data.find("add-friend", 0) :
        pass

   


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
    application.add_handler(CallbackQueryHandler(queryHandler))
    print("Application Running")
    application.run_polling()
    #will not run


if __name__  == "__main__" :
    main()

# Use Firefox instead of Chrome
