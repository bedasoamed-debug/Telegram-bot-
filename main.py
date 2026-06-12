import os
import telebot
import requests
from threading import Thread
from flask import Flask

# Flask Server uumuu (Render akka Port banamu arguuf)
app = Flask('')

@app.route('/')
def home():
    return "Bootiin AI Einstein toora irra jira!"

def run_flask():
    # Render ofumaan PORT nuuf kenna, yoo dhabame 8080 fayyadama
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Telegram Bot Setup (Token kee isa haaraa asitti galcheera)
token = os.getenv('BOT_TOKEN')
if not token:
    token = '8868692269:AAHZHSne3i2Y1eiQjR-DJDe7vuPrJYqD-eM'

bot = telebot.TeleBot(token)

# 📣 Odeeffannoo Chaanaalii Keetii
CHANNEL_ID = -1002394584458
CHANNEL_LINK = "https://t.me/beekkumsa_walii_galaa"

def check_status(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except Exception:
        return False

# AI irraa deebii fiduuf (Free API)
def get_ai_response(prompt):
    try:
        url = f"https://browser9.ddns.net/api/v1/chat/gpt-4o?text={prompt}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get("reply", "🧠 Deebii xiinxalaa jira. Mee deebisii na gaaftadhu!")
        else:
            return "🧠 Sammuun koo yeroo muraasaaf biredii fudhachaa jira. Mee xiqqoo eegiiti na gaaftadhu!"
    except Exception:
        return "🧠 Sarvarri AI yeroo muraasaaf hojii ala ta'eera. Mee booda na gaaftadhu."

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    if check_status(user_id):
        welcome_text = (
            f"👋 Akkam, {message.from_user.first_name}!\n\n"
            "Ani Bot Einstein haaraa ChatGPT k
