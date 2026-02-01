import os
import time
import concurrent.futures
from telegram.ext import Updater, CommandHandler
from instagrapi import Client

cl = Client()

def start(update, context):
    update.message.reply_text("🚩 Ravana Turbo Bot Active!\n/login username password\n/fire group_name")

def login_ig(update, context):
    try:
        user, pw = context.args[0], context.args[1]
        update.message.reply_text(f"🚀 Logging in as {user}...")
        cl.login(user, pw)
        update.message.reply_text(f"✅ Login Success!\nUser: {cl.account_info().username}")
    except Exception as e:
        update.message.reply_text(f"❌ Login Fail: {e}")

def turbo_send(target_id, message):
    # Fast sending logic
    try:
        cl.direct_send(message, thread_ids=[target_id])
    except:
        pass

def start_firing(update, context):
    try:
        group_query = " ".join(context.args)
        update.message.reply_text(f"🔍 Searching for: {group_query}...")
        
        # Target dhoondhna aur show karna
        threads = cl.direct_threads(15)
        target_thread = None
        for t in threads:
            if group_query.lower() in t.thread_title.lower():
                target_thread = t
                break
        
        if target_thread:
            # Telegram par Target Name show karna
            update.message.reply_text(f"🎯 Target Locked!\nName: {target_thread.thread_title}\nID: {target_thread.id}\n🔥 Turbo Firing Shuru...")
            
            msg = "﷽" * 50 # Chota message fast delivery ke liye
            
            # 1 second mein multiple messages (Threading)
            while True:
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    for _ in range(20):
                        executor.submit(turbo_send, target_thread.id, msg)
                time.sleep(0.5) # Minimum gap to avoid instant ban
        else:
            update.message.reply_text("❌ Target nahi mila!")
            
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

# Bot Setup
TOKEN = "TERA_TELEGRAM_TOKEN"
updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("login", login_ig))
dp.add_handler(CommandHandler("fire", start_firing))
updater.start_polling()
      
