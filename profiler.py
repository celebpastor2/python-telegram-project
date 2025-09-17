from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import CallbackContext, ContextTypes
import string
import random
import requests
from user import BASE_URL, PROVIDER_TOKEN
import json

async def queryHandler(update: Update, context:CallbackContext ):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    chat_id = update.effective_chat.id

    print(f" Query Data {query.data}")


    if query.data == "create-group" :
        group_id = generateTxt(10)
           
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
                [InlineKeyboardButton(text="Topup Balance", callback_data="topup-bal")]    
            ])

        await query.edit_message_text(f"First Name: {first_name}" f" \n Last Name: {last_name}" f" \n Phone number: {phone_number}" f" \n Username: {username}" f" \n Location: {location}" f" \n Balance: {balance}" , reply_markup=keyboard_markup)
    elif query.data.lower() == "topup-bal" :
        keyboard_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="$1", callback_data="load-one"), InlineKeyboardButton(text="$2", callback_data="load-two"), InlineKeyboardButton(text="$5", callback_data="load-five")],
             [InlineKeyboardButton(text="$10", callback_data="load-ten"), InlineKeyboardButton(text="$20", callback_data="load-twenty"), InlineKeyboardButton(text="$50", callback_data="load-fifty")],
              [InlineKeyboardButton(text="$100", callback_data="load-hundred"), InlineKeyboardButton(text="$200", callback_data="load-two-hundred"), InlineKeyboardButton(text="$500", callback_data="load-five-hundred")],
              [InlineKeyboardButton(text="$1000", callback_data="load-one-thousand"),InlineKeyboardButton(text="$2000", callback_data="load-two-thousand"), InlineKeyboardButton(text="$5000", callback_data="load-five-thousand")]
        ])

        await query.edit_message_text(text="Please click any of the button to load your balance", reply_markup=keyboard_markup)
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
                resp_text += f"\n {friend['username']} {friend['chat_id']}"
            
            resp_text  += f"\n chat with any friend using /message [friend_id] [message...]"
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
            
            for product in products["fields"]:
            
                text += f"name - {product['name']} price - ${product['price']} \n\n"

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

    else :
        await topup_balance(update=update,context=context)


async def topup_balance(update: Update, context: CallbackContext) :
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    chat_id = update.effective_chat.id
    payload = generateTxt(15)
    
    print(f"See Query Data {query.data}")
    try:
       
        
        if query.data == "load-five" :

            await query.message.reply_invoice(
                payload = payload,
                title   = "$5 Loading",
                description = "Payment for Loading $5 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $5", 500)],
                provider_token = PROVIDER_TOKEN
            )
        elif query.data == "load-ten" :
            await query.message.reply_invoice(
                chat_id = chat_id,
                payload = payload,
                title   = "$10 Loading",
                description = "Payment for Loading $10 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $10", 1000)],
                provider_token = PROVIDER_TOKEN
            )
        elif query.data == "load-twenty" :
            await query.message.reply_invoice(
                payload = payload,
                title   = "$20 Loading",
                description = "Payment for Loading $20 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $20", 2000)],
                provider_token = PROVIDER_TOKEN
            )
        elif query.data == "load-fifty" :
            await query.message.reply_invoice(
                payload = payload,
                title   = "$50 Loading",
                description = "Payment for Loading $50 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $50", 5000)],
                provider_token = PROVIDER_TOKEN
            )
        elif query.data == "load-hundred" :
            await query.message.reply_invoice(
                payload = payload,
                title   = "$100 Loading",
                description = "Payment for Loading $100 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $100", 10000)],
                provider_token = PROVIDER_TOKEN
            )
        elif query.data == "load-two-hundred" :
            await query.message.reply_invoice(
                payload = payload,
                title   = "$200 Loading",
                description = "Payment for Loading $200 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $200", 20000)],
                provider_token = PROVIDER_TOKEN
            )
        elif query.data == "load-five-hundred" :
            print("In loading five hundred...")
            await query.message.reply_invoice(
                payload = payload,
                title   = "$500 Loading",
                description = "Payment for Loading $500 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $500", 50000)],
                provider_token = PROVIDER_TOKEN
            )
        elif query.data == "load-one-thousand" :
            await query.message.reply_invoice(
                payload = payload,
                title   = "$1000 Loading",
                description = "Payment for Loading $1000 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $1000", 100000)],
                provider_token = PROVIDER_TOKEN
            )
        elif query.data == "load-two-thousand" :
            await query.message.reply_invoice(
                payload = payload,
                title   = "$2000 Loading",
                description = "Payment for Loading $2000 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $2000", 200000)],
                provider_token = PROVIDER_TOKEN
            )
        elif query.data == "load-five-thousand" :
            await query.message.reply_invoice(
                payload = payload,
                title   = "$5000 Loading",
                description = "Payment for Loading $5000 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $5000", 500000)],
                provider_token = PROVIDER_TOKEN
            )
        elif query.data == "load-one" :
            await query.message.reply_invoice(
                payload = payload,
                title   = "$1 Loading",
                description = "Payment for Loading $1 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $1", 100)],
                provider_token = PROVIDER_TOKEN
            )
        elif query.data == "load-two" :
            await query.message.reply_invoice(
                chat_id = chat_id,
                payload = payload,
                title   = "$2 Loading",
                description = "Payment for Loading $2 to Balance",
                need_email = True,
                need_name = True,
                need_phone_number = False,
                need_shipping_address = False,
                currency = "USD",
                prices = [LabeledPrice("Loading $2", 2)],
                provider_token = PROVIDER_TOKEN
            )
        #await update.message.reply_text(response.text) 
    
    except Exception as e:
        print(e)
        await query.edit_message_text("Topup balance does not exist")

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    payment = update.message.successful_payment
    user = update.message.from_user
    balance = payment.total_amount
    payload = payment.invoice_payload

    data = {
        "amount" : balance,
        "payload": payload,
        "chat_id":chat_id
    }

    endpoint = "/load-balance"

    response = requests.post(f"{BASE_URL}{endpoint}", data=data)

    try :
        userFr = json.loads(response.text)
        await update.message.reply_text(
            f"**Payment Successful**\n\n"
            f"Thank you for Purchasing Our Credit {user.username}\n\n"
            f"Your Purchased: ${payment.total_amount / 100}\n\n"
            f"Your transaction ID: {payment.telegram_payment_charge_id} \n\n"
            f"Your Balance is now: ${userFr['new_balance']}"


        )

    except :
        await update.message.reply_text(f"Payment Successful But Balance not Updated\n\n You can run /retry_payment {payload} to retry loading you balance. Note your payload ID: {payload}")


async def pre_checkout(update: Update, context: CallbackContext) :
    query       = update.pre_checkout_query
    chat_id     = query.from_user.id
    payload     =  query.invoice_payload
    shiping_add    = query.order_info.shipping_address
    email          = query.order_info.email
    name            = query.order_info.name
    phone_number    = query.order_info.phone_number
    description     = ""
    title           = ""
    currency        = query.currency
    price           = query.total_amount
    endpoint        = "/topup"

    data = {
        "chat_id":chat_id,
        "payload":payload,
        "name"  : name,
        "title" : title,
        "description":description,
        "email":email,
        "phone_number": phone_number,
        "shipping_address": shiping_add,
        "currency"  : currency,
        "price"     : price

    }

    requests.post(f"{BASE_URL}{endpoint}", data=data)
        
    await query.answer(ok=True)

def generateTxt(limit = 10) :
    letters = string.ascii_letters + string.digits
    group_id = ""
    for _ in range(limit) :
         group_id += str( random.choice(letters) )

    return group_id