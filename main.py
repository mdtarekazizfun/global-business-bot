import requests
import time
import json
import os

TOKEN = "7356961896:AAE6VukMLQ50odCEfzJJ2zaSM3laK0eKW9A"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"
REFERRAL_FILE = "referrals.json"
BALANCE_FILE = "balances.json"
MIN_WITHDRAW = 100
REWARD_PER_REF = 5

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    params = {"chat_id": chat_id, "text": text}
    requests.get(url, params=params)

def get_updates(offset=None):
    url = BASE_URL + "getUpdates"
    params = {"timeout": 30, "offset": offset}
    resp = requests.get(url, params=params).json()
    return resp.get("result", [])

def handle_update(update, referrals, balances):
    message = update.get("message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    user_id = str(chat_id)
    text = message.get("text", "")

    if text.startswith("/start"):
        parts = text.split()
        if len(parts) > 1:
            referrer_id = parts[1]
            if referrer_id != user_id:
                if referrer_id not in referrals:
                    referrals[referrer_id] = []
                if user_id not in referrals[referrer_id]:
                    referrals[referrer_id].append(user_id)
                    balances[referrer_id] = balances.get(referrer_id, 0) + REWARD_PER_REF
                    save_json(REFERRAL_FILE, referrals)
                    save_json(BALANCE_FILE, balances)

        send_message(chat_id,
            "🌟 Welcome to Global Business Bot!\n\n"
            "📌 DXN Business – One World One Market\n"
            "Want to open an account or learn business?\n"
            "🔗 https://eworld.dxn2u.com/s/accreg/en/827221982\n\n"
            "📝 Required Documents:\n"
            "1️⃣ National ID (Front & Back) or Passport (info page)\n"
            "2️⃣ Valid Email Address\n"
            "3️⃣ Active Mobile Number\n\n"
            "🔧 Need help? Contact Account Opener:\n"
            "👉 t.me/mdtarekazizfun\n\n"
            "👉 Use /Products to view our items\n"
            "👉 Use /Social to follow us online\n"
            "👉 Use /OfferAndReference for earnings & referral\n"
            "👉 Use /Office to get DXN info\n"
            "👉 Use /Help for assistance")

    elif text == "/Products":
        send_message(chat_id, "🛍️ Products:\nhttps://www.excellentworldint.com/products")

    elif text == "/Social":
        send_message(chat_id,
            "🌐 Social Media Links:\n\n"
            "📘 Facebook (Excellent): https://www.facebook.com/ExcellentWorldIntBD\n"
            "📘 Facebook (DXN): https://www.facebook.com/DXNGlobalBusinessBD\n"
            "📺 YouTube Channel: https://www.youtube.com/YouTubeBanglaMPTABD\n"
            "📱 IMO Group: https://s.channelcom.tech/Oe9jLm?from=copy_link\n"
            "📎 LinkedIn (Excellent): https://www.linkedin.com/company/excellentworldintbd/\n"
            "📎 LinkedIn (DXN): https://www.linkedin.com/company/dxnglobelbusiness/\n"
            "📢 Telegram Channel: https://t.me/excellentworldintbd\n"
            "👥 Telegram Group: https://t.me/OnlineAndOfflineEarningBD\n"
            "🔗 Facebook Group: https://facebook.com/groups/dreamrealizationbd/")

    elif text == "/Office":
        send_message(chat_id,
            "🏢 DXN Business Office:\n\n"
            "🔗 Account Open Link:\nhttps://eworld.dxn2u.com/s/accreg/en/827221982\n\n"
            "📄 Required:\n1️⃣ NID or Passport\n2️⃣ Email\n3️⃣ Phone\n\n"
            "📲 Open through: t.me/mdtarekazizfun")

    elif text == "/OfferAndReference":
        referred = referrals.get(user_id, [])
        count = len(referred)
        balance = balances.get(user_id, 0)
        ref_link = f"https://t.me/GlobalBusinessIntBot?start={user_id}"

        withdraw_text = "❌ Minimum ৳100 required for withdrawal."
        if balance >= MIN_WITHDRAW:
            withdraw_text = "✅ You are eligible to request withdrawal!"

        referred_users = "\n".join(referred) if referred else "No referrals yet."

        send_message(chat_id,
            f"🎁 Offer & Reference Info\n\n"
            f"🔗 Your Referral Link:\n{ref_link}\n\n"
            f"👥 Total Referrals: {count}\n"
            f"💰 Balance: ৳{balance}\n\n"
            f"{withdraw_text}\n"
            f"🧾 Referred Users:\n{referred_users}")

    elif text == "/Help":
        send_message(chat_id,
            "📖 Help Menu:\n\n"
            "🏠 /Start – Start the bot\n"
            "🛍️ /Products – View Products\n"
            "🌐 /Social – Social Media Links\n"
            "🏢 /Office – DXN Info\n"
            "🎁 /OfferAndReference – Earnings & Referrals\n"
            "💡 /Help – Help Message")

def run_bot():
    referrals = load_json(REFERRAL_FILE)
    balances = load_json(BALANCE_FILE)
    last_update = None
    while True:
        updates = get_updates(offset=last_update)
        for upd in updates:
            last_update = upd["update_id"] + 1
            handle_update(upd, referrals, balances)
        time.sleep(1)

if __name__ == "__main__":
    run_bot()
    
