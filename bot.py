import telebot
import optimize
from telebot import types
from sympy import symbols, Eq, solve, sympify
import sympy as sp
import re

# API-токен бота
BOT_TOKEN = "6562035500:AAGjA4qgoHN8CzrAhinOGThYX_o-Qk58-Gw"

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

userData = {}
    

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    oneDem = types.KeyboardButton("Методы одномерной оптимизации")
    grad = types.KeyboardButton("Градиентные методы поиска экстремума")
    secondOrder = types.KeyboardButton("Методы второго порядка")
    cond = types.KeyboardButton("Методы условной оптимизации")
    keyboard.add(oneDem, grad)
    keyboard.add(secondOrder, cond)
    bot.send_message(
        message.chat.id,
        'Привет! Я бот, который помогает решать оптимизационные задачи.\nДля начала выберите класс оптимизационных задач', 
        reply_markup=keyboard
    )
    bot.register_next_step_handler(message, choose_optimization_class)


def choose_optimization_class(message):
    opClass = message.text
    if opClass == "Методы одномерной оптимизации":
        oneDimensionOptimization(message)
    elif opClass == "Градиентные методы поиска экстремума":
        gradOptimization(message)
    elif opClass == "Методы второго порядка":
        secondOrderOptimization(message)
    elif opClass == "Методы условной оптимизации":
        conditionalOptimization(message)
    else:
        bot.send_message(message.chat.id, 'Что-то в моих закромах нет такого класса, попробуйте заново')


def gradOptimization(message):
    defaultAnswer(message)


def secondOrderOptimization(message):
    defaultAnswer(message)


def conditionalOptimization(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    penalty = types.KeyboardButton("Метод штрафов")
    barrier = types.KeyboardButton("Метод барьерных функций")
    keyboard.add(penalty, barrier)
    
    userData[message.chat.id] = {}
    bot.send_message(message.chat.id,'Выберите, каким методом найти минимум функции', reply_markup=keyboard)	
    bot.register_next_step_handler(message, choose_method)

def defaultAnswer(message):
    bot.send_message(message.chat.id, 'Я пока не умею такое решать, но скоро научусь!')

def oneDimensionOptimization(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    halfDiv = types.KeyboardButton("Метод половинного деления")
    gold = types.KeyboardButton("Метод золотого сечения")
    fib = types.KeyboardButton("Метод чисел Фибоначчи")
    keyboard.add(halfDiv, gold, fib)
    
    userData[message.chat.id] = {}
    bot.send_message(message.chat.id,'Выберите, каким методом найти минимум функции', reply_markup=keyboard)	
    bot.register_next_step_handler(message, choose_method)


def choose_method(message):
    text = message.text
    if text =="Метод половинного деления" or text == "Метод золотого сечения" or text == "Метод чисел Фибоначчи":
        chooseOneDimMethod(message)
    elif text == "Метод штрафов" or "Метод барьерных функций":
        save_lim_method(message)
    else:
        bot.send_message(message.chat.id, "Что-то я такого метода не знаю(")


def save_lim_method(message):
    userData[message.chat.id]['type'] = message.text
    bot.send_message(message.chat.id, "Введите формулу. Например 6*x^2+2*z^2-25", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, save_equation_2)


def save_equation_2(message):
    if check_equation(message):
        userData[message.chat.id]['equation'] = message.text
        bot.send_message(message.chat.id, "Введите ограничение типа равенство. Например 10*x+z-7=0")
        bot.register_next_step_handler(message, save_lim)
    else:
        bot.send_message(message.chat.id, "Что-то вы не то ввели. Попробуйте еще раз. Например 6*x^2+2*z^2-25")
        bot.register_next_step_handler(message, save_equation_2)

def save_lim(message):
    if check_equation(message):
        userData[message.chat.id]['lim'] = message.text
        bot.send_message(message.chat.id, "Введите E. Например 0.05")
        bot.register_next_step_handler(message, save_epsilon_2)
    else:
        bot.send_message(message.chat.id, "Что-то вы не то ввели. Попробуйте еще раз. Например 10*x+z-7=0")
        bot.register_next_step_handler(message, save_lim)

def save_epsilon_2(message):
    text = message.text
    if check_epsilon(text, message):
        userData[message.chat.id]['e'] = text
        bot.send_message(message.chat.id, "Введите r. Например 0.5")
        bot.register_next_step_handler(message, save_r)
    else:
        bot.send_message(message.chat.id, "Что-то вы не то ввели. Попробуйте еще раз. Например 0.05")
        bot.register_next_step_handler(message, save_epsilon_2)

def save_r(message):
    text = message.text
    if check_epsilon(text, message):
        userData[message.chat.id]['r'] = text
        bot.send_message(message.chat.id, "Введите C. Например 8")
        bot.register_next_step_handler(message, save_c)
    else:
        bot.send_message(message.chat.id, "Что-то вы не то ввели. Попробуйте еще раз. Например 0.5")
        bot.register_next_step_handler(message, save_r)

def save_c(message):
    text = message.text
    if message.text.isdigit():
        userData[message.chat.id]['c'] = text
        bot.send_message(message.chat.id, optimize.minimize(userData[message.chat.id], message.chat.id))
        try:
            # Отправляем HTML-файл пользователю
            with open("./media/index.html", 'rb') as html:
                bot.send_document(message.chat.id, html)
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")
    else:
        bot.send_message(message.chat.id, "Что-то вы не то ввели. Попробуйте еще раз. Например 8")
        bot.register_next_step_handler(message, save_r)


def chooseOneDimMethod(message):
    userData[message.chat.id]['type'] = message.text
    bot.send_message(message.chat.id, "Введите формулу. Например sin(x)*x^2", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, save_equation)


def save_equation(message):
    if check_equation(message):
        userData[message.chat.id]['equation'] = message.text
        bot.send_message(message.chat.id, "Введите точность E. Например 0.4")
        bot.register_next_step_handler(message, save_epsilon)
    else:
        bot.send_message(message.chat.id, "Что-то вы не то ввели. Попробуйте еще раз. Например sin(x)*x^2")
        bot.register_next_step_handler(message, save_equation)


def check_equation(message):
    try:
        eq = sympify(message.text)
    except sp.SympifyError:
        return False
    return True
        

def save_epsilon(message):
    text = message.text
    if check_epsilon(text, message):
        userData[message.chat.id]['e'] = text
        bot.send_message(message.chat.id, "Введите интервал L. Например 0;6")
        bot.register_next_step_handler(message, saveInterval)
    else:
        bot.send_message(message.chat.id, "Что-то вы не то ввели. Попробуйте еще раз. Например 0.4")
        bot.register_next_step_handler(message, save_epsilon)


def check_epsilon(text, message):
    try:
        float(text)
        return True
    except ValueError:
        return False


def saveInterval(message):
    text = message.text
    if re.fullmatch(r'^\d+;\d+$', text):
        l = text.split(";")
        if float(l[0]) <= float(l[1]):
            chat_id = message.chat.id
            userData[chat_id]['l'] = message.text
            bot.send_message(chat_id, optimize.minimize(userData[chat_id], chat_id))
            method = userData[chat_id]['type']
            file_path = f'media/{chat_id}_{method}.gif'
            gif = open(file_path, 'rb')
            bot.send_video(chat_id, gif, None, 'Text')
            gif.close()
        else:
            bot.send_message(message.chat.id, "Что-то вы не то ввели. Попробуйте еще раз. Например 0;6")
            bot.register_next_step_handler(message, saveInterval)
    else:
        bot.send_message(message.chat.id, "Что-то вы не то ввели. Попробуйте еще раз. Например 0;6")
        bot.register_next_step_handler(message, saveInterval)

# Запуск бота
bot.polling()
