import imghdr
import time
import concurrent.futures
from telegram.ext import Updater, CommandHandler
from instagrapi import Client

cl = Client()

# Telegram Bot Token yahan dalo
TOKEN = "7976862323:AAE23Kwygfeu_yH-TDhVkwJ5HqyMZVqo5pw"

def start(update, context):
    update.message.reply_text("🚩 Ravana Turbo Bot Active!\n/login username password\n/fire group_name")

def login_ig(update, context):
    try:
        user, pw = context.args[0], context.args[1]
        update.message.reply_text(f"🚀 Logging in as {user}...")
        cl.login(user, pw)
        update.message.reply_text(f"✅ Login Success! Connected as: {cl.account_info().username}")
    except Exception as e:
        update.message.reply_text(f"❌ Login Fail: {e}")

def turbo_send(target_id, message):
    try:
        cl.direct_send(message, thread_ids=[target_id])
    except:
        pass

def start_firing(update, context):
    try:
        group_query = " ".join(context.args)
        update.message.reply_text(f"🔍 Searching for target: {group_query}...")
        
        threads = cl.direct_threads(15)
        target_thread = next((t for t in threads if group_query.lower() in t.thread_title.lower()), None)
        
        if target_thread:
            update.message.reply_text(f"🎯 Target Locked: {target_thread.thread_title}\n🔥 Infinite Turbo Firing Shuru...")
            msg = "﷽" * 50
            while True:
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    for _ in range(20):
                        executor.submit(turbo_send, target_thread.id, msg)
                time.sleep(0.5)
        else:
            update.message.reply_text("❌ Target nahi mila!")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("login", login_ig))
dp.add_handler(CommandHandler("fire", start_firing))
updater.start_polling()
      
