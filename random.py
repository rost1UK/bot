import telebot
import random
import string
import os
import subprocess
import sys

# Автоматическая установка библиотеки, если её нет
try:
    import telebot
except ImportError:
    print("Устанавливаю pyTelegramBotAPI...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI"])
    import telebot

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ Добавь TOKEN в Variables на Railway!")

bot = telebot.TeleBot(TOKEN)

FIRST_LETTER = os.getenv("FIRST_LETTER", "X")
LETTERS = string.ascii_uppercase
user_first = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_first[message.from_user.id] = True
    bot.send_message(message.chat.id,
        f"🔥 <b>English Uppercase Letter Bot</b> 🔥\n\n"
        f"Первая буква: <b>{FIRST_LETTER}</b>\n"
        f"Команды:\n"
        f"/letter — одна буква\n"
        f"/string 40 — строка из 40 букв\n"
        f"/setfirst Z — сменить первую букву",
        parse_mode='HTML')

@bot.message_handler(commands=['letter'])
def send_letter(message):
    if user_first.get(message.from_user.id, True):
        bot.send_message(message.chat.id, f"🎯 Первая: <b>{FIRST_LETTER}</b>", parse_mode='HTML')
        user_first[message.from_user.id] = False
    else:
        bot.send_message(message.chat.id, f"🔠 <b>{random.choice(LETTERS)}</b>")

@bot.message_handler(commands=['string'])
def send_string(message):
    try:
        n = int(message.text.split()[1])
        n = max(5, min(n, 400))
    except:
        n = 30
    text = ''.join(random.choice(LETTERS) for _ in range(n))
    bot.send_message(message.chat.id, f"📜 <b>{text}</b>")

@bot.message_handler(commands=['setfirst'])
def set_first(message):
    try:
        new = message.text.split()[1][0].upper()
        if new in LETTERS:
            global FIRST_LETTER
            FIRST_LETTER = new
            bot.reply_to(message, f"✅ Первая буква теперь <b>{FIRST_LETTER}</b>")
    except:
        bot.reply_to(message, "Пример: /setfirst A")

print("🚀 Бот запущен...")
bot.infinity_polling()