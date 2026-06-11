import os
import telebot
from telebot import types

# Token sirriitti Render Environment Variables irraa akka dubbisu gochuuf
token = os.getenv('BOT_TOKEN')
if not token:
    # Yoo Render irratti hin galchine ta'e, kiiyoo kee kanaan ofumaan akka eegalu gochuuf:
    token = '8868692269:AAH_Q4fZ0F5ne3oe2ZcpvfE1CTG4o4UMGJI'

bot = telebot.TeleBot(token)

# Ajaja /start yeroo cuqaasan ergaa jalqabaa uumuuf
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        f"👋 Akkam, {message.from_user.first_name}!\n\n"
        "Ani Bot Chat haasaa keeti. Mee waan sitti tolu kamiyyuu naaf barreessi, "
        "ani ammoo ofumaan siif deebisa! 🤖✨"
    )
    bot.reply_to(message, welcome_text)

# Ergaa barreeffamaa (Text) namoonni ergan hunda fudhatte deebisuuf
@bot.message_handler(content_types=['text'])
def echo_all(message):
    user_message = message.text.lower()
    
    # Fakeenyaf deebiiwwan ofumaan deebi'an (Custom Chat Responses)
    if user_message in ['akkam', 'selam', 'hello', 'hi']:
        reply = f"Akkam jirtu {message.from_user.first_name}? Fayyaadha? Ati maalin si gargaaru?"
    elif user_message in ['fayyaa', 'fayyaadha', 'gaariidha']:
        reply = "Galatoomi! Akka ati gaarii jirtu dhaga'uun koo na gammachiisa. 😊"
    elif user_message in ['maqaan kee eenyu', 'maqaan kee']:
        reply = "Maqaan kiyya Chat Bot jedhama, koodii Python kanaan hojjetame!"
    elif user_message in ['galatoomi', 'galatomaa', 'thanks']:
        reply = "Homaa miti! Yoomiyyuu si gargaaruuf qophiidha. 🌟"
    else:
        # Yoo barreeffama biraa ta'e, ergaa isaa deebisee "Echo" godha
        reply = f"Ergaa kee: '{message.text}' jedhu sirriitti dubbiseera! 🧠"

    bot.reply_to(message, reply)

# Yoo namni kofla (Sticker) ykn fulaa koflaa ergeef
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    bot.reply_to(message, "Wow, sticker baredaa dha! 👍😍")

# ZAPUSK BOTA (Infinity Polling)
if __name__ == '__main__':
    print("Bootiin Chat jalqabaa jira...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Dogoggorri uumameera: {e}")
