import telebot

TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 123456789  # آیدی خودت

bot = telebot.TeleBot(TOKEN)

# ذخیره موقت کاربران و بلاک‌ها
users = set()
blocked = set()
reply_map = {}

# START
@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.chat.id)
    bot.send_message(message.chat.id,
    "👋 خوش اومدی!\nپیام بفرست تا ناشناس برای ادمین ارسال بشه.")

# بلاک کردن (فقط ادمین)
@bot.message_handler(commands=['block'])
def block_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            user_id = int(message.text.split()[1])
            blocked.add(user_id)
            bot.send_message(ADMIN_ID, f"🚫 بلاک شد: {user_id}")
        except:
            bot.send_message(ADMIN_ID, "❌ استفاده: /block user_id")

# پیام‌ها
@bot.message_handler(content_types=['text', 'photo', 'voice', 'video', 'audio'])
def handle(message):
    if message.chat.id in blocked:
        return

    users.add(message.chat.id)

    # ارسال به ادمین
    caption = f"📩 پیام جدید از: {message.chat.id}"

    if message.content_type == 'text':
        sent = bot.send_message(ADMIN_ID, f"{caption}\n\n{message.text}")

    elif message.content_type == 'photo':
        sent = bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption)

    elif message.content_type == 'voice':
        sent = bot.send_voice(ADMIN_ID, message.voice.file_id, caption=caption)

    elif message.content_type == 'video':
        sent = bot.send_video(ADMIN_ID, message.video.file_id, caption=caption)

    elif message.content_type == 'audio':
        sent = bot.send_audio(ADMIN_ID, message.audio.file_id, caption=caption)

    # ذخیره برای ریپلای
    reply_map[sent.message_id] = message.chat.id

# ریپلای ادمین به کاربر
@bot.message_handler(func=lambda m: m.reply_to_message and m.chat.id == ADMIN_ID)
def reply(message):
    original = message.reply_to_message.message_id

    if original in reply_map:
        user_id = reply_map[original]

        bot.send_message(user_id, f"💬 پاسخ ادمین:\n\n{message.text}")

bot.polling()
