import requests
import time
import json
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

TOKEN = "7356961896:AAE6VukMLQ50odCEfzJJ2zaSM3laK0eKW9A"
REFERRAL_FILE = "referrals.json"
BALANCE_FILE = "balances.json"
MIN_WITHDRAW = 100
MIN_REFERRALS = 20
REWARD_PER_REF = 5
ADMIN_ID = 123456789  # Replace with your Telegram user ID

# --- JSON File Handling ---
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

# --- Command Handlers ---
def start(update, context):
    user = update.message.from_user
    user_id = str(user.id)
    referrals = load_json(REFERRAL_FILE)
    balances = load_json(BALANCE_FILE)

    args = context.args
    if args:
        referrer_id = args[0]
        if referrer_id != user_id:
            if referrer_id not in referrals:
                referrals[referrer_id] = []
            if user_id not in referrals[referrer_id]:
                referrals[referrer_id].append(user_id)
                balances[referrer_id] = balances.get(referrer_id, 0) + REWARD_PER_REF
                save_json(REFERRAL_FILE, referrals)
                save_json(BALANCE_FILE, balances)

    total_refs = len(referrals.get(user_id, []))
    ref_link = f"https://t.me/GlobalBusinessIntBot?start={user_id}"

    keyboard = [
        [InlineKeyboardButton("🛍 Products", callback_data='products'), InlineKeyboardButton("🌐 Social", callback_data='social')],
        [InlineKeyboardButton("🎁 Offer & Reference", callback_data='offer'), InlineKeyboardButton("🏢 Office", callback_data='office')],
        [InlineKeyboardButton("💡 Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "👋 Welcome to Global Business Bot 💹\n\n"
        "📌 Start your international business journey for FREE!\n"
        "🧾 Create a DXN/Excellent account and earn by referrals.\n"
        "💸 Earn ৳5 per referral. Withdraw when you reach ৳100 from 20 referrals.\n\n"
        f"🔗 Your Referral Link: {ref_link}\n"
        f"👥 Total Referrals: {total_refs}\n\n"
        "🔧 Need help? Contact: @mdtarekazizfun"
    )
    update.message.reply_text(welcome_text, reply_markup=reply_markup)

def button_handler(update, context):
    query = update.callback_query
    query.answer()
    data = query.data
    chat_id = query.message.chat.id

    if data == 'products':
        context.bot.send_message(chat_id, "🛍️ Products: https://www.excellentworldint.com/products")
    elif data == 'social':
        context.bot.send_message(chat_id,
            "🌐 Social Media Links:\n\n"
            "📘 Facebook (Excellent): https://facebook.com/ExcellentWorldIntBD\n"
            "📘 Facebook (DXN): https://facebook.com/DXNGlobalBusinessBD\n"
            "📺 YouTube: https://youtube.com/YouTubeBanglaMPTABD\n"
            "📱 IMO: https://s.channelcom.tech/Oe9jLm\n"
            "📎 LinkedIn (Excellent): https://linkedin.com/company/excellentworldintbd/\n"
            "📎 LinkedIn (DXN): https://linkedin.com/company/dxnglobelbusiness/\n"
            "📢 Telegram Channel: https://t.me/excellentworldintbd\n"
            "👥 Telegram Group: https://t.me/OnlineAndOfflineEarningBD\n"
            "🔗 Facebook Group: https://facebook.com/groups/dreamrealizationbd/")
    elif data == 'office':
        context.bot.send_message(chat_id,
            "🏢 DXN Business Office Info:\n\n"
            "📌 DXN Business – One World One Market\n"
            "🔗 Account Link: https://eworld.dxn2u.com/s/accreg/en/827221982\n\n"
            "📝 Required:\n1️⃣ NID or Passport\n2️⃣ Email\n3️⃣ Phone\n\n"
            "📲 Contact: @mdtarekazizfun")
    elif data == 'offer':
        user_id = str(chat_id)
        referrals = load_json(REFERRAL_FILE)
        balances = load_json(BALANCE_FILE)
        referred = referrals.get(user_id, [])
        count = len(referred)
        balance = balances.get(user_id, 0)
        ref_link = f"https://t.me/GlobalBusinessIntBot?start={user_id}"

        if count >= MIN_REFERRALS and balance >= MIN_WITHDRAW:
            context.bot.send_message(chat_id,
                f"🎁 Your Referral Info:\n\n"
                f"🔗 Referral Link: {ref_link}\n👥 Total Referrals: {count}\n💰 Balance: ৳{balance}\n\n"
                f"✅ You're eligible to withdraw.\n"
                f"✍️ Send the following info:\n- Bkash/Nagad Number\n- Name\n- Amount\n- Note (if any)")
        else:
            context.bot.send_message(chat_id,
                f"🎁 Your Referral Info:\n\n"
                f"🔗 Referral Link: {ref_link}\n👥 Total Referrals: {count}\n💰 Balance: ৳{balance}\n\n"
                f"❌ You need at least 20 referrals and ৳100 to request withdrawal.")
    elif data == 'help':
        context.bot.send_message(chat_id,
            "💡 Help Menu:\n\n"
            "/start – Start the bot\n"
            "/Products – View Products\n"
            "/Social – Social Media Links\n"
            "/Office – DXN Info\n"
            "/OfferAndReference – Earnings & Referrals\n"
            "/Help – Help Message")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, lambda update, ctx: None))
    dp.add_handler(MessageHandler(Filters.command, lambda update, ctx: None))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
