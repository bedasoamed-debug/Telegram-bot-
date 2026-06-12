import os
import telebot
import requests

token = os.getenv('BOT_TOKEN')
if not token:
    token = '8868692269:AAH_Q4fZ0F5ne3oe2ZcpvfE1CTG4o4UMGJI'

bot = telebot.TeleBot(token)

# 📣 Odeeffannoo Chaanaalii Keetii (Amma Sirreeffameera)
# ID chaanaalii kee isa duraanii saniin wal qabsiisneera
CHANNEL_ID = -1002394584458
CHANNEL_LINK = "https://t.me/beekkumsa_walii_galaa"

# Namni sun chaanaalii kee keessa jiru fi jiraachuu baachuu isaa mirkaneessuuf
def check_status(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except Exception:
        return False

# AI irraa deebii fiduuf
def get_ai_response(prompt):
    try:
        url = f"https://browser9.ddns.net/api/v1/chat/gpt-4o?text={prompt}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get("reply", "🧠 Of dhowwadhu, deebii xiinxalaa jira. Mee deebisii na gaaftadhu!")
        else:
            return "🧠 Sammuun koo yeroo muraasaaf biredii fudhachaa jira. Mee deebisii na gaaftadhu!"
    except Exception:
        return "🧠 Dogoggorri uumameera. Mee xiqqoo eegiiti na gaaftadhu."

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    if check_status(user_id):
        welcome_text = (
            f"👋 Akkam, {message.from_user.first_name}!\n\n"
            "Ani Bot Einstein haaraa ChatGPT kanaan hojjedhu dha. "
            "Gaaffii qabdu kamiyyuu na gaaftadhu, sirriitti siif nan deebisa! 🧠✨"
        )
        bot.reply_to(message, welcome_text)
    else:
        bot.reply_to(message, f"🚀 Bootii kana fayyadamuuf, jalqaba chaanaalii keenya join godhaa:\n\n{CHANNEL_LINK}")

@bot.message_handler(content_types=['text'])
def handle_ai_chat(message):
    user_id = message.from_user.id
    
    # 1. Dirqama chaanaalii join gochuu isaa eeggachuu
    if not check_status(user_id):
        bot.reply_to(message, f"🚀 Bootii kana fayyadamuuf, jalqaba chaanaalii keenya join godhaa:\n\n{CHANNEL_LINK}")
        return

    user_query = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    # 2. AI irraa deebii fiduu
    ai_response = get_ai_response(user_query)
    bot.reply_to(message, ai_response)

if __name__ == '__main__':
    print("Bootiin AI Chat guutummaatti jalqabaa jira...")
    bot.infinity_polling()
