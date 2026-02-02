import time
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from instagrapi import Client

cl = Client()
TOKEN = "7976862323:AAE23Kwygfeu_yH-TDhVkwJ5HqyMZVqo5pw"

def start(update, context):
    update.message.reply_text("🚩 Ravana Bot Active!\nUse /login [session_id]")

def login_ig(update, context):
    try:
        session_id = context.args[0]
        cl.login_by_sessionid(session_id)
        
        threads = cl.direct_threads(10)
        buttons = [[InlineKeyboardButton(t.thread_title, callback_data=f"gr_{t.id}")] for t in threads if t.thread_title]
        
        update.message.reply_text("✅ Login Success! Group chuno:", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        update.message.reply_text(f"❌ Login Fail: {e}")

def handle_click(update, context):
    query = update.callback_query
    data = query.data
    
    if data.startswith("gr_"):
        group_id = data.split("_")[1]
        # Yahan name change logic
        try:
            # Sahi function for Wi-Fi/Server bypass
            cl.direct_thread_title_set(group_id, "RAVANA WAS HERE")
            query.edit_message_text("🚀 Instagram Group Name Changed!")
        except Exception as e:
            query.edit_message_text(f"❌ Insta ne Block kiya: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("login", login_ig))
    dp.add_handler(CallbackQueryHandler(handle_click))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
    
      
