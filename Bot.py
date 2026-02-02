import time
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from instagrapi import Client

cl = Client()
TOKEN = "7976862323:AAE23Kwygfeu_yH-TDhVkwJ5HqyMZVqo5pw" # Apna asli token yahan sahi se dalo

def start(update, context):
    update.message.reply_text("🚩 Ravana Ultra Active!\nUse: /login [session_id]")

def login_ig(update, context):
    try:
        session_id = context.args[0]
        update.message.reply_text("🚀 Logging in...")
        cl.login_by_sessionid(session_id)
        
        # Login ke baad saare groups (threads) nikalna
        threads = cl.direct_threads(20) # Top 20 groups/chats
        buttons = []
        for thread in threads:
            if thread.thread_title: # Sirf groups dikhane ke liye
                buttons.append([InlineKeyboardButton(thread.thread_title, callback_data=f"group_{thread.id}")])
        
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text("✅ Login Success! Saare Groups niche hain, kispe 'Fire' karna hai select karo:", reply_markup=reply_markup)
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

def button_click(update, context):
    query = update.callback_query
    data = query.data
    if data.startswith("group_"):
        group_id = data.split("_")[1]
        context.user_data['target_group'] = group_id
        
        # Speed Selection Buttons
        speed_buttons = [
            [InlineKeyboardButton("Slow (10s)", callback_data="speed_10"),
             InlineKeyboardButton("Medium (5s)", callback_data="speed_5"),
             InlineKeyboardButton("Fast (1s)", callback_data="speed_1")]
        ]
        query.edit_message_text("⚡ Speed select karo:", reply_markup=InlineKeyboardMarkup(speed_buttons))

# Isme aage message count aur firing ka logic add kar sakte hain

      
