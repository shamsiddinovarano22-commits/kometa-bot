import telebot
import os
import json

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID  = int(os.environ.get("ADMIN_ID"))

bot = telebot.TeleBot(BOT_TOKEN)
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    bot.send_message(
        message.chat.id,
        "👋 Assalomu alaykum!\n\n"
        "🌯 Kometa Fast Food botiga xush kelibsiz!\n"
        "Buyurtma berish uchun quyidagi tugmani bosing 👇"
    )

# Admin yuborganda — bot nomidan hammaga ketadi
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID,
                     content_types=['text', 'photo', 'video'])
def broadcast(message):
    users = load_users()
    ok, fail = 0, 0
    for user_id in users:
        if user_id == ADMIN_ID:
            continue
        try:
            bot.copy_message(user_id, ADMIN_ID, message.message_id)
            ok += 1
        except:
            fail += 1
    bot.send_message(ADMIN_ID, f"✅ Yuborildi: {ok} ta\n❌ Xato: {fail} ta")

# Foydalanuvchi yozsa — adminga ketadi
@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID,
                     content_types=['text', 'photo', 'video'])
def forward_to_admin(message):
    save_user(message.chat.id)
    bot.copy_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "✅ Xabaringiz qabul qilindi!")

bot.polling(none_stop=True)
