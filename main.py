import telebot
from telebot import types


# 5395666619:AAEO-jO96JY3gWq0QwPAJfNjlJsZevNwnrw
token = "5395666619:AAEO-jO96JY3gWq0QwPAJfNjlJsZevNwnrw"
bot = telebot.TeleBot(token)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    msg = bot.reply_to(message, """\
Рады приветствовать вас в нашем бот-опросе! Отправьте любое сообщение, чтобы начать.
""",reply_markup=markup)
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Мужской', 'Женский')
        msg = bot.reply_to(message, 'Укажите свой пол:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_age_step)



def process_age_step(message):
        chat_id = message.chat.id
        age = message.text
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('до 21', 'от 21 до 30','от 30')
        msg = bot.reply_to(message, 'Укажите свой возраст:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_place_step)


def process_place_step(message):
    chat_id = message.chat.id
    age = message.text
    user = user_dict[chat_id]
    user.age = age
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('учусь', 'работаю')
    msg = bot.reply_to(message, 'Вы работаете или учитесь?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_place_of_step)

def process_place_of_step(message):
    chat_id = message.chat.id
    text = message.text
    if text == u'учусь':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('школа', 'университет/колледж')
        msg = bot.reply_to(message, 'В каком учебном заведении вы учитесь?', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('да', 'нет')
        msg = bot.reply_to(message, 'Связана ли сфера, в которой вы работаете с программированием?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_salary_step)

def process_salary_step(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('отсутствует', 'от 35к до 60к','от 60к и больше')
    msg = bot.reply_to(message, 'Какая у вас заработная плата на данный момент?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_waste_step)

def process_waste_step(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('0', 'от 1к до 5к','от 5к и 10к', 'от 10к и больше')
    msg = bot.reply_to(message, 'Сколько вы готовы тратить на курс?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_step)

def process_step(message):
    msg = bot.reply_to(message, """\
    Спасибо, что приняли участие в нашем опросе.
    """)

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()