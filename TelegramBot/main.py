import telebot
from telebot import types
import botsetting as bs
from prediction import get_visual_prediction
from analytics import *
from ConversationChoice import *
import os
import random
import re

bot = telebot.TeleBot(bs.config['token'])

def validate_user_input(input_string):
    pattern = re.compile(r'^\d{4},.*\w+$')
    return  pattern.match(input_string)

def validate_input_for_flaps(user_input):
    pattern = re.compile(r'^\d{4},\s*\w+,\s*\d+,\s*\d+$')
    return pattern.match(user_input)

def get_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Предсказание", callback_data= "Предсказание")
    button2 = types.InlineKeyboardButton("Аналитика", callback_data= 'Аналитика')
    button3 = types.InlineKeyboardButton("Помощь", callback_data='Помощь')
    keyboard.add(button1, button2, button3)
    return keyboard

def process_points_input(message):
    if not validate_user_input(message.text):
        text = random.choice(not_validate_input)
        bot.send_message(message.chat.id, text, parse_mode='html')
        bot.register_next_step_handler(message, process_points_input)
    else:
        text = random.choice(information_research)
        bot.send_message(message.chat.id, text, parse_mode='html')
        text = message.text.split(', ')
        year, granprix = int(text[0]), text[1]
        output = get_visual_prediction(year, granprix)
        if output == -1:
            bot.send_message(message.chat.id, random.choice(lack_of_data), parse_mode='html')
        else:
            bot.send_photo(message.chat.id, photo=open(output, 'rb'))
            os.remove(output)
        keyboard = get_keyboard()
        bot.send_message(message.chat.id, 'Что дальше?)', parse_mode='html', reply_markup=keyboard)

def import_pole(message):
    output = importancepole(message.text)
    if output != -1:
        bot.send_message(message.chat.id, 'На данной трассе, побеждали с поул позиции в ' + str(output) + '% случаев', parse_mode='html')
    else:
        bot.send_message(message.chat.id, random.choice(lack_of_data), parse_mode='html')
    
    keyboard = get_keyboard()
    bot.send_message(message.chat.id, 'Что дальше?)', parse_mode='html', reply_markup=keyboard)

def compare_fasterslaps(message):
    if not validate_input_for_flaps(message.text):
        text = random.choice(not_validate_input)
        bot.send_message(message.chat.id, text, parse_mode='html')
        bot.register_next_step_handler(message, compare_fasterslaps)
    else:
        text = random.choice(information_research)
        bot.send_message(message.chat.id, text, parse_mode='html')
        text = message.text.split(', ')
        year, granprix, driver_1, driver_2 = int(text[0]), text[1], text[2], text[3]
        output = comparefastestlaps(year, granprix ,driver_1, driver_2)
        if output == -1:
            bot.send_message(message.chat.id, random.choice(lack_of_data), parse_mode='html')
        else:
            bot.send_photo(message.chat.id, photo=open(output, 'rb'))
            os.remove(output)
        keyboard = get_keyboard()
        bot.send_message(message.chat.id, 'Что дальше?)', parse_mode='html', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help(message):
    keyboard = get_keyboard()
    bot.send_message(message.chat.id, 'Так-так, я могу:', parse_mode='html', reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = get_keyboard()
    out_text = '{hello}\n<b>{user_name}</b> Вы написали {bot_name}\nЯ ваш верный друг в исследовании данных по Формуле 1'.format(
        hello=random.choice(hello_say),
        user_name=message.from_user.first_name,
        bot_name=bs.config['name'])
    bot.send_message(message.chat.id, out_text, parse_mode='html')
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "Предсказание":
        points(call.message)
    elif call.data == "Аналитика":
        analysis(call.message)
    elif call.data == 'Помощь':
        help(call.message)

@bot.message_handler(commands=['points'])
def points(message):
    bot.send_message(message.chat.id, "Чтобы получить прогноз просто напиши мне год и название трассы через запятую\nНапример: 2023, Imola")
    bot.register_next_step_handler(message, process_points_input)


@bot.message_handler(commands=['analysis'])
def analysis(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Важность поул позиции📈")
    button2 = types.KeyboardButton("Сравнение быстрых кругов💥")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def handle_button_click(message):
    remove_keyboard = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Что ж давай посмотрим...", reply_markup=remove_keyboard)
    if message.text == "Важность поул позиции📈":
        bot.send_message(message.chat.id, "Введите место, где расположанна трасса")
        bot.register_next_step_handler(message, import_pole)
    elif message.text == "Сравнение быстрых кругов💥":
        bot.send_message(message.chat.id, "Чтобы получить сравнение просто напиши мне год и название трассы через запятую и номера гонщиков\nНапример: 2023, Imola, 16, 55\n")
        bot.register_next_step_handler(message, compare_fasterslaps)

@bot.message_handler(content_types=['text'])
def text(message):
    text = 'Извини, я тебя не понимаю'
    bot.send_message(message.chat.id, text, parse_mode='html')
    keyboard = get_keyboard()
    bot.send_message(message.chat.id, 'Выбери команду', parse_mode='html', reply_markup=keyboard)


bot.polling(non_stop=True, interval=0)