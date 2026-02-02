import time
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from instagrapi import Client

cl = Client()
# Apna asli TOKEN yahan sahi se dalo
TOKEN = "7976862323:AAE23Kwygfeu_yH-TDhVkwJ5HqyMZVqo5pw" 

def start(update, context):
    update.message.reply_text("🚩 Ravana Ultra Active!\nUse: /login [session_id]")

def login_ig(update, context):
    try:
        session_id = context.args[0]
        update.message.reply_text("🚀 Logging in...")
        cl.login_by_sessionid(session_id)
        
        threads = cl.direct_threads(15) # Top 15 groups
        buttons = []
        for thread in threads:
            if thread.thread_title:
                buttons.append([InlineKeyboardButton(thread.thread_title, callback_data=f"group_{thread.id}")])
        
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text("✅ Login Success! Group select karo:", reply_markup=reply_markup)
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

def button_click(update, context):
    query = update.callback_query
    query.answer()
    data = query.data
    
    if data.startswith("group_"):
        context.user_data['target'] = data.split("_")[1]
        speed_buttons = [
            [InlineKeyboardButton("Slow (10s)", callback_data="sp_10"),
             InlineKeyboardButton("Medium (5s)", callback_data="sp_5"),
             InlineKeyboardButton("Fast (1s)", callback_data="sp_1")]
        ]
        query.edit_message_text("⚡ Speed select karo:", reply_markup=InlineKeyboardMarkup(speed_buttons))
    
    elif data.startswith("sp_"):
        speed = int(data.split("_")[1])
        query.edit_message_text(f"🚀 Firing started with {speed}s delay! (Restart bot to stop)")
        # Yahan apna message firing loop chala sakte ho

# YE WALI LINES SABSE ZAROORI HAIN (Inhe mat bhoolna)
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("login", login_ig))
    dp.add_handler(CallbackQueryHandler(button_click))
    
    updater.start_polling()
    updater.idle() # Bot ko zinda rakhega

if __name__ == '__main__':
    main()
    
      
