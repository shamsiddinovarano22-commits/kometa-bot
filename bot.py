import telebot
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID  = os.environ.get("ADMIN_ID")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Assalomu alaykum!\n\n"
        "🌯 Kometa Fast Food botiga xush kelibsiz!\n"
        "Buyurtma berish uchun quyidagi tugmani bosing 👇"
    )
    bot.send_message(
        int(ADMIN_ID),
        f"🔔 Yangi foydalanuvchi!\n"
        f"👤 Ism: {message.from_user.first_name}\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"📱 Username: @{message.from_user.username}"
    )

@bot.message_handler(func=lambda m: True)
def forward_to_admin(message):
    bot.forward_message(int(ADMIN_ID), message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "✅ Xabaringiz qabul qilindi!")

bot.polling(none_stop=True)
