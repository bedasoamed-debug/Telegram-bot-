# amatsukami
Telegram Bot for adding members to the club from CRMI (Pavlodar city)

git add requirements.txt
git commit -m "Add requirements.txt"
git push


import telebot
from telebot import types
from datetime import datetime

token = '8868692269:AAH_Q4fZ0F5ne3oe2ZcpvfE1CTG4o4UMGJI'
bot = telebot.TeleBot(token)

# Хранилище для данных
GROUP_CHAT_ID = '-1002828257881'  # ⚠️ Замените на правильный ID группы!
user_data = {}
completed_registrations = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("Вступить")
    btn2 = types.KeyboardButton("Правила")
    btn3 = types.KeyboardButton("Адрес")
    markup.add(btn1, btn2, btn3)

    bot.send_message(
        message.chat.id,
        f"Добро пожаловать, {message.from_user.first_name}! Выберите опцию:",
        reply_markup=markup
    )

@bot.message_handler(commands=['getid'])
def get_chat_id(message):
    chat_id = message.chat.id
    bot.send_message(message.chat.id, f"ID этого чата: {chat_id}")
    print(f"ID чата: {chat_id}")

# Обработчик для кнопок
@bot.message_handler(content_types=['text'])
def handle_buttons(message):
    if message.text == "Вступить":
        user_id = message.from_user.id
        
        # Проверяем, не заполнял ли пользователь уже анкету
        if user_id in completed_registrations:
            show_existing_application(message)
            return
            
        bot.send_message(message.chat.id, "📝 Переходим к заполнению анкеты...")
        start_registration(message)
        
    elif message.text == "Правила":
        bot.send_message(
            message.chat.id,
            """📋 В чате запрещаются:

•Оскорбления. Помните, что даже шуточные оскорбления могут задеть.

•Спам. Сюда входят бессмысленные сообщения, одинаковые стикеры, ссылки без контекста и частые повторы.

•Обсуждение политики/религии и других острых тем.

•Расизм/сексизм/гомофобия.

•Разжигание конфликтов. 

•Реклама/пиар. Прежде чем скинуть рекламу, необходимо согласовать ее с администрацией.

•18+ контент. Любые стикеры/гифки/сообщения на эту тему строго запрещены


📋 Правила поведения в кабинете:

1. В кабинете строго запрещены алкоголь и сигареты, вейпы. 

2.Соблюдайте правила безопасности и внимательно относитесь к своим вещам: не оставляйте личные вещи без присмотра и следите за своим имуществом. Администрация не несёт ответственности за чужие вещи.

3. Если возникают конфликты или недопонимания, решайте их мирным путем, при необходимости обращайтесь к администрации.

4. Кабинет могут открывать только администрация и волонтеры.

5. Поддерживайте чистоту: убирайте за собой и не оставляйте мусор.

6. Уважайте личное пространство и время других: не прерывайте работу без необходимости.

7. В кабинете запрещается приносить и употреблять продукты с резким запахом (лапшу быстрого приготовления, латяо, колбасу, чеснок и т.д). Вы всегда можете перекусить, но просим вас выбирать нейтральные по запаху продукты. 

8. В кабинете есть общие кружки (они подписаны), из которых вы можете пить. Убедительная просьба — не трогать кружки волонтеров или администрации. Не забывайте мыть посуду после использования!

9. Соблюдайте тишину. Администрация или волонтеры вправе закрыть кабинет из-за сильного шума.

10. Нецензурная лексика запрещена.


 ❗️За нарушение правил администрация имеет право дать предупреждение. 3 предупреждение — удаление из группы. Наша цель — создать тёплую, безопасную и приятную атмосферу общения в беседе.
            """
        )
        
    elif message.text == "Адрес":
        bot.send_message(message.chat.id, 
    """📍 Наш адрес: Ломова 38(ЦРМИ)
 Кабинет 009.
 Находится на цокольном этаже, в корпусе С.

❗️ Как найти кабинет:
 
 Войдите через центральный вход, пройдите прямо, поверните налево и спуститесь вниз по лестнице. Кабинет находится справа."""
        )

def show_existing_application(message):
    """Показывает ранее заполненную анкету"""
    user_id = message.from_user.id
    data = completed_registrations[user_id]
    
    work_study_display = format_work_study_display(data)
    
    existing_app_text = f"""
⚠️ Вы уже заполняли анкету!

📋 Ваша анкета:
┌─────────────────────
│ 👤 ФИО: {data['fio']}
│ 🎂 Дата рождения: {data['birthdate']} ({data['age']} лет)
│ {work_study_display}
└─────────────────────

Ваша анкета находится в обработке. С вами свяжутся в ближайшее время.
"""
    
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, existing_app_text, reply_markup=markup)
    
    import time
    time.sleep(3)
    welcome(message)

# 🎯 ФУНКЦИИ ДЛЯ АНКЕТЫ

def start_registration(message):
    """Начало заполнения анкеты"""
    user_id = message.from_user.id
    user_data[user_id] = {}  # Создаем запись для пользователя
    
    # Убираем клавиатуру с кнопками
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Подготовка...", reply_markup=markup)
    
    # Запрашиваем ФИО
    msg = bot.send_message(
        message.chat.id,
        "📝 Введите ваше ФИО (полностью):"
    )
    bot.register_next_step_handler(msg, process_fio)

def process_fio(message):
    """Обработка ФИО"""
    user_id = message.from_user.id
    user_data[user_id]['fio'] = message.text
    
    # Запрашиваем дату рождения
    msg = bot.send_message(message.chat.id, "Дата рождения (в формате ДД.ММ.ГГГГ):")
    bot.register_next_step_handler(msg, process_birthdate)

def is_valid_date(date_string):
    """Проверка правильности формата даты"""
    try:
        # Проверяем базовый формат
        if len(date_string) != 10 or date_string[2] != '.' or date_string[5] != '.':
            return False
        
        day, month, year = date_string.split('.')
        
        # Проверяем, что все части - числа
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            return False
        
        # Проверяем диапазоны
        day = int(day)
        month = int(month) 
        year = int(year)
        
        if not (1 <= month <= 12):
            return False
        if not (1 <= day <= 31):
            return False
        if not (1900 <= year <= 2024):
            return False
            
        return True
    except:
        return False

def calculate_age(birth_date):
    """Вычисление возраста по дате рождения"""
    today = datetime.now()
    age = today.year - birth_date.year
    
    # Проверяем, был ли уже день рождения в этом году
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    
    return age

def process_birthdate(message):
    """Обработка даты рождения"""
    user_id = message.from_user.id
    
    # Проверяем формат даты
    if not is_valid_date(message.text):
        msg = bot.send_message(
            message.chat.id, 
            "❌ Неверный формат даты! Пожалуйста, введите в формате ДД.ММ.ГГГГ:\n\n"
            "Например: 01.01.2000"
        )
        bot.register_next_step_handler(msg, process_birthdate)
        return
    
    user_data[user_id]['birthdate'] = message.text
    
    # Вычисляем возраст
    birth_date = datetime.strptime(message.text, '%d.%m.%Y')
    user_data[user_id]['age'] = calculate_age(birth_date)
    
    # Запрашиваем место обучения/работы
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎓 Учусь", "💼 Работаю", "📚 И то, и то", "🚫 Ничего из этого")
    
    msg = bot.send_message(
        message.chat.id,
        "🎯 Ваш текущий статус:",
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, process_status_choice)

def process_status_choice(message):
    """Обработка выбора статуса"""
    user_id = message.from_user.id
    choice = message.text
    user_data[user_id]['status_choice'] = choice
    
    if choice == "🎓 Учусь":
        ask_education_type(message)
        
    elif choice == "💼 Работаю":
        ask_work_place(message)
        
    elif choice == "📚 И то, и то":
        user_data[user_id]['work_study'] = {}  # Создаем словарь для обоих
        ask_education_type(message)  # Сначала про учёбу
        
    elif choice == "🚫 Ничего из этого":
        user_data[user_id]['work_study'] = "—"  # Прочерк
        # Сразу завершаем анкету
        show_summary(message)

def ask_education_type(message):
    """Тип учебного заведения"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🏫 Школа", "🎓 Колледж", "🏛️ Институт", "🎓 Университет")
    
    msg = bot.send_message(
        message.chat.id,
        "🎓 Где вы учитесь?",
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, process_education_type)

def process_education_type(message):
    """Обработка типа учебного заведения"""
    user_id = message.from_user.id
    education_type = message.text
    user_data[user_id]['education_type'] = education_type
    
    # Запрашиваем название учебного заведения
    markup = types.ReplyKeyboardRemove()
    msg = bot.send_message(
        message.chat.id,
        "📝 Напишите название учебного заведения:",
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, process_education_name)

def process_education_name(message):
    """Обработка названия учебного заведения"""
    user_id = message.from_user.id
    education_name = message.text
    
    # Сохраняем данные в зависимости от контекста
    if user_data[user_id]['status_choice'] == "📚 И то, и то":
        user_data[user_id]['work_study']['education'] = {
            'type': user_data[user_id]['education_type'],
            'name': education_name
        }
    else:
        user_data[user_id]['work_study'] = {
            'type': user_data[user_id]['education_type'],
            'name': education_name
        }
    
    # Запрашиваем класс/курс в зависимости от типа
    if user_data[user_id]['education_type'] == "🏫 Школа":
        ask_school_grade(message)
    else:
        ask_course(message)

def ask_school_grade(message):
    """Запрос класса для школы"""
    msg = bot.send_message(
        message.chat.id,
        "🔢 В каком вы классе? (только цифра):\n\n"
        "Например: 9, 10, 11"
    )
    bot.register_next_step_handler(msg, process_school_grade)

def process_school_grade(message):
    """Обработка класса школы"""
    user_id = message.from_user.id
    
    # Проверяем, что введена цифра
    if not message.text.isdigit():
        msg = bot.send_message(
            message.chat.id,
            "❌ Пожалуйста, введите только цифру (класс):\n\n"
            "Например: 9, 10, 11"
        )
        bot.register_next_step_handler(msg, process_school_grade)
        return
    
    grade = message.text
    
    # Сохраняем класс
    if user_data[user_id]['status_choice'] == "📚 И то, и то":
        user_data[user_id]['work_study']['education']['grade'] = grade
    else:
        user_data[user_id]['work_study']['grade'] = grade
    
    # Переходим к следующему шагу
    if user_data[user_id]['status_choice'] == "📚 И то, и то":
        ask_work_place(message)  # После учёбы спрашиваем про работу
    else:
        # Завершаем анкету для "Учусь"
        show_summary(message)

def ask_course(message):
    """Запрос курса для колледжа/института/университета"""
    msg = bot.send_message(
        message.chat.id,
        "🎓 На каком вы курсе? (только цифра):\n\n"
        "Например: 1, 2, 3, 4"
    )
    bot.register_next_step_handler(msg, process_course)

def process_course(message):
    """Обработка курса"""
    user_id = message.from_user.id
    
    # Проверяем, что введена цифра
    if not message.text.isdigit():
        msg = bot.send_message(
            message.chat.id,
            "❌ Пожалуйста, введите только цифру (курс):\n\n"
            "Например: 1, 2, 3, 4"
        )
        bot.register_next_step_handler(msg, process_course)
        return
    
    course = message.text
    
    # Сохраняем курс
    if user_data[user_id]['status_choice'] == "📚 И то, и то":
        user_data[user_id]['work_study']['education']['course'] = course
    else:
        user_data[user_id]['work_study']['course'] = course
    
    # Переходим к следующему шагу
    if user_data[user_id]['status_choice'] == "📚 И то, и то":
        ask_work_place(message)  # После учёбы спрашиваем про работу
    else:
        # Завершаем анкету для "Учусь"
        show_summary(message)

def ask_work_place(message):
    """Запрос места работы"""
    msg = bot.send_message(
        message.chat.id,
        "💼 Где вы работаете?\n\n"
        "Напишите название организации:"
    )
    bot.register_next_step_handler(msg, process_work_place)

def process_work_place(message):
    """Обработка места работы"""
    user_id = message.from_user.id
    work_place = message.text
    
    # Сохраняем данные в зависимости от контекста
    if user_data[user_id]['status_choice'] == "📚 И то, и то":
        user_data[user_id]['work_study']['work'] = work_place
    else:
        user_data[user_id]['work_study'] = work_place
        
    # Завершаем анкету
    show_summary(message)

def format_work_study_display(data):
    """Форматирование для показа пользователю"""
    work_study = data['work_study']
    status = data['status_choice']
    
    if status == "🎓 Учусь":
        if data['education_type'] == "🏫 Школа":
            return f"🎓 Учёба: {work_study['name']}\n📚 Класс: {work_study['grade']}"
        else:
            return f"🎓 Учёба: {work_study['name']}\n📚 Курс: {work_study['course']}"
    
    elif status == "💼 Работаю":
        return f"💼 Работа: {work_study}"
    
    elif status == "📚 И то, и то":
        education = work_study['education']
        work = work_study['work']
        
        if education['type'] == "🏫 Школа":
            return f"🎓 Учёба: {education['name']}\n📚 Класс: {education['grade']}\n💼 Работа: {work}"
        else:
            return f"🎓 Учёба: {education['name']}\n📚 Курс: {education['course']}\n💼 Работа: {work}"
    
    else:
        return f"💼 Статус: {work_study}"

def format_work_study_group(data):
    """Форматирование для отправки в группу"""
    work_study = data['work_study']
    status = data['status_choice']
    
    if status == "🎓 Учусь":
        if data['education_type'] == "🏫 Школа":
            return f"│ 🎓 Учёба: {work_study['name']}\n│ 📚 Класс: {work_study['grade']}\n"
        else:
            return f"│ 🎓 Учёба: {work_study['name']}\n│ 📚 Курс: {work_study['course']}\n"
    
    elif status == "💼 Работаю":
        return f"│ 💼 Работа: {work_study}\n"
    
    elif status == "📚 И то, и то":
        education = work_study['education']
        work = work_study['work']
        
        if education['type'] == "🏫 Школа":
            return f"│ 🎓 Учёба: {education['name']}\n│ 📚 Класс: {education['grade']}\n│ 💼 Работа: {work}\n"
        else:
            return f"│ 🎓 Учёба: {education['name']}\n│ 📚 Курс: {education['course']}\n│ 💼 Работа: {work}\n"
    
    else:
        return f"│ 💼 Статус: {work_study}\n"

def show_summary(message):
    """Показ итогов анкеты пользователю"""
    user_id = message.from_user.id
    data = user_data[user_id]
    
    work_study_display = format_work_study_display(data)
    
    summary_text = f"""
✅ РЕГИСТРАЦИЯ ЗАВЕРШЕНА!

📋 Ваша анкета:
┌─────────────────────
│ 👤 ФИО: {data['fio']}
│ 🎂 Дата рождения: {data['birthdate']} ({data['age']} лет)
│ {work_study_display}
└─────────────────────

Спасибо за регистрацию! Ваша анкета находится в обработке.
"""
    
    bot.send_message(message.chat.id, summary_text)
    
    # Сохраняем в завершенные анкеты
    completed_registrations[user_id] = data.copy()
    
    # Отправляем в группу
    send_to_group(message, data)
    
    # Возвращаем основное меню через 3 секунды
    import time
    time.sleep(3)
    welcome(message)

def send_to_group(message, user_data):
    """Отправка анкеты в группу"""
    work_study_text = format_work_study_group(user_data)
    
    username = f"@{message.from_user.username}" if message.from_user.username else "без username"
    
    group_message = f"""
📋 НОВАЯ АНКЕТА

👤 Пользователь: {username}
📱 Имя в TG: {message.from_user.first_name}
🆔 ID: {message.from_user.id}
┌─────────────────────
│ ФИО: {user_data['fio']}
│ Дата рождения: {user_data['birthdate']} ({user_data['age']} лет)
{work_study_text}└─────────────────────

⏰ Время регистрации: {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
    
    try:
        # Отправляем в группу
        bot.send_message(GROUP_CHAT_ID, group_message)
        print(f"✅ Анкета отправлена в группу для {user_data['fio']}")
    except Exception as e:
        print(f"❌ Ошибка отправки в группу: {e}")

# ЗАПУСК БОТА
if __name__ == '__main__':
    print("Бот запускается...")
    print("Перейдите в Telegram и напишите /start боту")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")
