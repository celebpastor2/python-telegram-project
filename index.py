from selenium import webdriver
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os

TELEGRAM_TOKEN = "7936586039:AAFBxzXW78tq9OArvZm5BfQiBPM3Kuta0C0"

#optional 
logging.basicConfig(
    filename="telegram.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)


#required
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(text=f"Hello {user.first_name}! This is Your Facebook Assistant \n This Assistant will help you to be more effective in using your Facebook Account, and can help your Business grow.\n Use /login [username] [password] to login to your account now!")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try :
        [username, password ] = context.args
        driver = webdriver.Chrome()

        SERVER = "https://facebook.com"

        try: 
            driver.get(SERVER)
            time.sleep(2)
            title = driver.title

            print(f"this is the title of a crawled website {title}")

            user_field = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "email")))
            pass_field = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "pass")))
            login_btn = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button")))

            user_field.send_keys(username)
            pass_field.send_keys(password)

            login_btn.click()
            #/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[1]/div/span[2]/span/div/span/span

            try :
                check_block = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[3]/div/div/div[2]/div/div/div[2]/span")))
                check_instruction = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[1]/div/span[2]/span/div/span/span")))

                await update.message.reply_text(f"Error Processing Login, Please Do The Following To Continue \n {check_instruction.text}")
            except Exception as e :
                url = driver.current_url
                
                try : 
                    url.index("privacy_mutation_token") 
                    await update.message.reply_text("Wrong Credential Supplied")
                except :
                    await update.message.reply_text(f"Login Successful, You can now this bot to make your Facebook account more profitable for you. Use with the following command: \n\n /see_friend [friend_name]  \n /text_friend [friend_name] [message] message should be in () \n /post_video [file_url] \n /post_photo [file_url] \n /add_friend [friend_name] \n /buy_product [product_name] ")
                    
                








            

        except Exception as e:
            print("Exception Occurred Here! ", e)
    except ValueError as e:
        await update.message.reply_text(text=f"Please enter in this format /login [username] [password] without the []")

    except Exception as e:
        print(f"error logging in {e}")
        await update.message.reply_text(text=f"Error Processing Your Request")

        driver.quit()

#used to start the application
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=message))
    application.add_handler(CallbackQueryHandler(button))
    print("Application Running")
    application.run_polling()
    #will not run


if __name__  == "__main__" :
    main()

# Use Firefox instead of Chrome
