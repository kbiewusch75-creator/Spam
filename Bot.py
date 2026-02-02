import time
import concurrent.futures
from telegram.ext import Updater, CommandHandler
from instagrapi import Client

cl = Client()

# Telegram Bot Token yahan dalo
TOKEN = "7976862323:AAE23Kwy gfeu_y..." # Tera purana token hi rehne dena

def start(update, context):
    update.message.reply_text("🚩 Ravana Turbo Bot Active!\n/login session_id\n/fire group_name")

def login_ig(update, context):
    try:
        session_id = context.args[0] # Ab ye password nahi, Session ID lega
        update.message.reply_text(f"🚀 Logging in with Session ID...")
        cl.login_by_sessionid(session_id)
        update.message.reply_text("✅ Login Success!")
    except Exception as e:
        update.message.reply_text(f"❌ Login Fail: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("login", login_ig))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
      
