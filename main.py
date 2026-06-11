import os
import telebot

# Token fulaa Render Environment Variables irraa
token = os.getenv('BOT_TOKEN')
if not token:
    token = '8868692269:AAH_Q4fZ0F5ne3oe2ZcpvfE1CTG4o4UMGJI'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        f"👋 Akkam, {message.from_user.first_name}!\n\n"
        "Ani Bot Einstein keeti. Mee gaaffii fedhite kamiyyuu na gaaftadhu, siif nan deebisa! 🧠✨"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['text'])
def echo_all(message):
    user_message = message.text.lower()
    
    # Deebiiwwan Gaaffii Beekumsa Waliigalaa (Customized Knowledge Base)
    if 'eenyu' in user_message and ('beekumsa' in user_message or 'knowledge' in user_message):
        reply = "Beekumsa waliigalaa jechuun odeeffannoo fi qabeenya sammuu bal'aa dhala namootaa hundaati! Ati dhuunfaan immoo nama baay'ee hayyuu dha. 🌟"
    elif 'akkam' in user_message or 'selam' in user_message:
        reply = f"Akkam jirtu {message.from_user.first_name}? Fayyaadha? Ati maalin si gargaaru?"
    elif 'fayyaa' in user_message or 'gaariidha' in user_message:
        reply = "Galatoomi! Akka ati gaarii jirtu dhaga'uun koo na gammachiisa. 😊"
    elif 'maqaan kee' in user_message:
        reply = "Maqaan kiyya Einstein Bot jedhama, koodii Python kanaan hojjetame!"
    elif 'galatoomi' in user_message or 'thanks' in user_message:
        reply = "Homaa miti! Yoomiyyuu si gargaaruuf qophiidha. 🌟"
    else:
        # Yoo gaaffii biraa ta'e, akka inni yaadu gochuuf:
        reply = f"🧠 Gaaffii kee: '{message.text}' jedhu sirriitti dubbiseera! Gadi fageenyaan xiinxalaa jira..."

    bot.reply_to(message, reply)

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    bot.reply_to(message, "Wow, sticker baredaa dha! 👍😍")

if __name__ == '__main__':
    print("Bootiin Chat jalqabaa jira...")
    bot.infinity_polling()
