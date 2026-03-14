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

@bot.message_handler(commands=['send'])
def broadcast(message):
    if message.chat.id != ADMIN_ID:
        return
    text = message.text.replace("/send ", "")
    users = load_users()
    ok, fail = 0, 0
    for user_id in users:
        try:
            bot.send_message(user_id, text)
            ok += 1
        except:
            fail += 1
    bot.send_message(ADMIN_ID, f"✅ Yuborildi: {ok}\n❌ Xato: {fail}")

@bot.message_handler(func=lambda m: True)
def forward_to_admin(message):
    if message.chat.id == ADMIN_ID:
        return
    save_user(message.chat.id)
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

bot.polling(none_stop=True)
```

---

## Ishlatish:

Botga xabar yuborish uchun **o'zingiz** botga yozing:
```
/send Assalomu alaykum! Bugun yangi aksiya bor 🔥
