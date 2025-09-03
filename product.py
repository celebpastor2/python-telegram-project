from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from telegram.ext import ContextTypes
from user import BASE_URL, ADS_LINK
import json

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

