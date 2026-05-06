import telebot
import random
import string
import os

# ←←← ВСТАВЬ СВОЙ ТОКЕН СЮДА ←←←
TOKEN = "8763070059:AAEEwrgXTv4Rv0QgppLyG4hX0g9EDt7N4Nw" 

bot = telebot.TeleBot(TOKEN)

FIRST_LETTER = "X"
LETTERS = string.ascii_uppercase
user_first = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_first[message.from_user.id] = True
    bot.send_message(message.chat.id, 
        f"🔥 <b>English Uppercase Bot</b> 🔥\n\n"
        f"Первая буква: <b>{FIRST_LETTER}</b>\n"
        f"/letter — одна буква\n"
        f"/string 30 — строка\n"
        f"/setfirst Z — сменить первую",
        parse_mode='HTML')

@bot.message_handler(commands=['letter'])
def letter(message):
    if user_first.get(message.from_user.id, True):
        bot.send_message(message.chat.id, f"🎯 Первая: <b>{FIRST_LETTER}</b>", parse_mode='HTML')
        user_first[message.from_user.id] = False
    else:
        bot.send_message(message.chat.id, f"🔠 <b>{random.choice(LETTERS)}</b>")

@bot.message_handler(commands=['string'])
def string_cmd(message):
    try:
        n = int(message.text.split()[1])
        n = max(5, min(n, 300))
    except:
        n = 25
    text = ''.join(random.choice(LETTERS) for _ in range(n))
    bot.send_message(message.chat.id, f"📜 <b>{text}</b>")

print("Бот запущен...")
bot.infinity_polling()
