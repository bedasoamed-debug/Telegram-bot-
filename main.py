import os
import telebot
from aient import chatgpt  # Library AI koodii kee keessaa

# Telegram Bot Token
token = os.getenv('BOT_TOKEN')
if not token:
    token = '8868692269:AAH_Q4fZ0F5ne3oe2ZcpvfE1CTG4o4UMGJI'

bot = telebot.TeleBot(token)

# AI ChatGPT Engine Initialize gochuuf (Token kee sirriitti as seeneera)
ai_bot = chatgpt(api_key="8868692269:AAH_Q4fZ0F5ne3oe2ZcpvfE1CTG4o4UMGJI", engine="gpt-4o")

# 📣 Odeeffannoo Chaanaalii Keetii
CHANNEL_ID = -1002394584458  # ID Chaanaalii keetii
CHANNEL_LINK = "https://t.me/beekkumsa_walii_galaa"  # Liinkii Chaanaalii keetii

# Namni sun chaanaalii kee keessa jiraachuu isaa mirkaneessuuf
def check_status(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except Exception:
        return False

# Ajaja /start yeroo eegalan
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    if check_status(user_id):
        welcome_text = (
            f"👋 Akkam, {message.from_user.first_name}!\n\n"
            "Ani Bot Einstein haaraa ChatGPT-4o kanaan hojjedhu dha. "
            "Gaaffii qabdu kamiyyuu na gaaftadhu, sirriitti siif nan deebisa! 🧠✨"
        )
        bot.reply_to(message, welcome_text)
    else:
        bot.reply_to(message, f"🚀 Bootii kana fayyadamuuf, jalqaba chaanaalii keenya join godhaa:\n\n{CHANNEL_LINK}")

# Ergaa barreeffamaa (Text) hunda AI biraan gahuuf
@bot.message_handler(content_types=['text'])
def handle_ai_chat(message):
    user_id = message.from_user.id
    
    # 1. Dirqama chaanaalii join gochuu isaa eeggachuu
    if not check_status(user_id):
        bot.reply_to(message, f"🚀 Bootii kana fayyadamuuf, jalqaba chaanaalii keenya join godhaa:\n\n{CHANNEL_LINK}")
        return

    # 2. Yoo chaanaalii keessa jiraate, AI irraa deebii barbaaduu jalqaba
    user_query = message.text
    
    # Botichi oomishaa akka jiru argisiisuuf "Typing..." action fiduu
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # AI (ChatGPT) gaaffii namichaa gaafachuu
        ai_response = ai_bot.ask(user_query)
        
        # Deebii AI irraa dhufe namaaf deebisuu
        bot.reply_to(message, ai_response)
    except Exception as e:
        bot.reply_to(message, "🧠 Of dhowwadhu, sammuun koo yeroo muraasaaf biredii fudhachaa jira. Mee deebisii na gaaftadhu!")
        print(f"AI Error: {e}")

if __name__ == '__main__':
    print("Bootiin AI Chat guutummaatti jalqabaa jira...")
    bot.infinity_polling()
