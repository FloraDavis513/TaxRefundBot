#!/usr/bin/python
# -*- coding: utf8 -*-

import telebot
import config
from telebot import types
import os
 
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    # abs_path = os.path.abspath('bot.py')
    # print(abs_path)
    # abs_path_new = abs_path.replace('\\', '/')
    # print(abs_path_new)
    # abs_path_new = abs_path_new[:abs_path_new.rindex('/')]
    # print(abs_path_new)
    # with open(f'{abs_path_new}/log.txt', 'a', encoding='utf-8') as g:
    with open(f'log.txt', 'a', encoding='utf-8') as g:
        print(f'{str(message.from_user.username)}\n{str(message.from_user.first_name)}\n{str(message.from_user.last_name)}\n{str(message.from_user.id)}\n\n', file=g)

    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = types.KeyboardButton("Меню")
    markup_menu.add(menu)

    bot.send_message(message.chat.id, config.WELCOME_MESSAGE, reply_markup=markup_menu)

@bot.message_handler(commands=['stop'])
def stop_info(message):
    bot.send_message(message.chat.id, config.STOP_MESSAGE)

@bot.message_handler(commands=['help'])
def help_info(message):
    bot.send_message(message.chat.id, config.COMMAND_LIST)

@bot.message_handler(commands=['feedback'])
def feedback(message):
    bot.register_next_step_handler(message, send_feedback)
    bot.send_message(message.chat.id, '''Введите свой отзыв''')

def send_feedback(message):
    if message.text != '':
        bot.send_message(503168284, f'''Фидбек от пользователя {str(message.from_user.first_name)} {str(message.from_user.last_name)}({str(message.from_user.id)}) получен:''')
        bot.send_message(503168284, message.text)
        bot.send_message(message.chat.id, '''Фидбек отправлен''')

@bot.message_handler(commands=['instruction'])
def instruction(message):
    bot.send_message(message.chat.id, config.INSTRUCTION_MESSAGE)
    doc = open('c:/Users/Alex/Desktop/Bot/test_file.txt', 'rb')
    bot.send_document(message.chat.id, doc)

@bot.message_handler(commands=['test'])
def test(message):
    markup_resident = types.InlineKeyboardMarkup(row_width=2)
    yes_button = types.InlineKeyboardButton("Да", callback_data='resident')
    no_button = types.InlineKeyboardButton("Нет", callback_data='not_resident')
    markup_resident.add(yes_button, no_button)
    bot.send_message(message.chat.id, config.IS_RESIDENT, reply_markup=markup_resident)

@bot.message_handler(commands=['standard'])
def standard(message):
    bot.send_message(message.chat.id, config.STANDARD_MESSAGE)

@bot.message_handler(commands=['get_standard'])
def get_standard(message):
    bot.send_message(message.chat.id, config.GET_STANDARD_MESSAGE)

@bot.message_handler(commands=['property'])
def property(message):
    bot.send_message(message.chat.id, config.PROPERTY_MESSAGE)

@bot.message_handler(commands=['get_property'])
def get_property(message):
    bot.send_message(message.chat.id, config.GET_PROPERTY_MESSAGE)

@bot.message_handler(commands=['investment'])
def investment(message):
    bot.send_message(message.chat.id, config.INVESTMENT_MESSAGE)

@bot.message_handler(commands=['get_investment_type_A'])
def investment_type_A(message):
    bot.send_message(message.chat.id, config.INVESTMENT_MESSAGE_A)

@bot.message_handler(commands=['social'])
def instruction(message):
    bot.send_message(message.chat.id, config.SOCIAL_MESSAGE_1)
    bot.send_message(message.chat.id, config.SOCIAL_MESSAGE_2)

@bot.message_handler(commands=['get_social'])
def get_social(message):
    bot.send_message(message.chat.id, config.GET_SOCIAL_MESSAGE)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'resident':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=config.IS_RESIDENT,
                reply_markup=None)
                markup_income = types.InlineKeyboardMarkup(row_width=2)
                yes_button = types.InlineKeyboardButton("Да", callback_data='has_income')
                no_button = types.InlineKeyboardButton("Нет", callback_data='not_income')
                markup_income.add(yes_button, no_button)
                bot.send_message(call.message.chat.id, config.INCOME_MESSAGE, reply_markup=markup_income)
            elif call.data == 'not_resident':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=config.IS_RESIDENT,
                reply_markup=None)
                bot.send_message(call.message.chat.id, config.REJECT_MESSAGE_1)
            elif call.data == 'has_income':
                bot.send_message(call.message.chat.id, config.REFUND_MESSAGE_INFO)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=config.INCOME_MESSAGE,
                reply_markup=None)
            elif call.data == 'not_income':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=config.INCOME_MESSAGE,
                reply_markup=None)
                bot.send_message(call.message.chat.id, config.REJECT_MESSAGE_2)
    except Exception as e:
        print(repr(e))
    return True

@bot.message_handler(content_types=['text'])
def undefined_input(message):
    if message.text == 'Меню':
            bot.send_message(message.chat.id, config.COMMAND_LIST)
    else:
        bot.send_message(message.chat.id, config.IDK)

# RUN
bot.polling(none_stop=True)
