import os
import telebot

token = os.getenv('BOT_TOKEN')
if not token:
    token = '8868692269:AAH_Q4fZ0F5ne3oe2ZcpvfE1CTG4o4UMGJI'

bot = telebot.TeleBot(token)

# 📣 Odeeffannoo Chaanaalii Keetii:
CHANNEL_ID = -1002394584458  # ID chaanaalii keetii asirratti sirriitti galeera
CHANNEL_LINK = "https://t.me/A_ToolsX"  # Liinkii chaanaalii keetii asirratti jijjiirachuu dandeessa

# Namni sun chaanaalii kee keessa jiraachuu isaa mirkaneessuuf
def check_status(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except Exception:
        # Yoo botichi chaanaalicha keessatti Admin ta'uu baate ykn dogoggorri uumame
        return False

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    if check_status(user_id):
        welcome_text = f"👋 Akkam, {message.from_user.first_name}!\n\nAni Bot Einstein keeti. Gaaffii fedhite na gaaftadhu! 🧠"
        bot.reply_to(message, welcome_text)
    else:
        # Yoo chaanaalii kee Join gochuu baate ergaa kana fida
        bot.reply_to(message, f"🚀 Bootii kana fayyadamuuf, jalqaba chaanaalii keenya join godhaa:\n\n{CHANNEL_LINK}")

@bot.message_handler(content_types=['text'])
def echo_all(message):
    user_id = message.from_user.id
    
    # Ergaa hunda dura dirqama chaanaalii kee keessa jiraachuu isaa ilaala
    if not check_status(user_id):
        bot.reply_to(message, f"🚀 To use this bot, you must join our channel:\n\n{CHANNEL_LINK}")
        return

    user_message = message.text.lower
