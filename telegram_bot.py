#!/usr/bin/python
# -*- coding: utf8 -*-

import telebot
import telegram_config
from telebot import types
import re
from datetime import datetime


 
bot = telebot.TeleBot(telegram_config.TOKEN)

last_income = 0
prev_prev_last_income = 0
prev_prev_prev_last_income = 0
invest_duration = 0
property_cost = 0

@bot.message_handler(commands=['start'])
def welcome(message):
    with open(f'log.txt', 'a', encoding='utf-8') as g:
        print(f'{str(message.from_user.username)}\n{str(message.from_user.first_name)}\n{str(message.from_user.last_name)}\n{str(message.from_user.id)}\n\n', file=g)
    bot.send_message(message.chat.id, telegram_config.WELCOME_MESSAGE)

@bot.message_handler(commands=['stop'])
def stop_info(message):
    bot.send_message(message.chat.id, telegram_config.STOP_MESSAGE)

@bot.message_handler(commands=['help'])
def help_info(message):
    bot.send_message(message.chat.id, telegram_config.COMMAND_LIST)






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
    bot.send_message(message.chat.id, telegram_config.INSTRUCTION_MESSAGE)
    doc = open('c:/Users/Alex/Desktop/Bot/TaxRefundBot/test_file.txt', 'rb')
    bot.send_document(message.chat.id, doc)







@bot.message_handler(commands=['test'])
def test(message):
    markup_resident = types.InlineKeyboardMarkup(row_width=2)
    yes_button = types.InlineKeyboardButton("Да", callback_data='test_resident')
    no_button = types.InlineKeyboardButton("Нет", callback_data='test_not_resident')
    markup_resident.add(yes_button, no_button)
    bot.send_message(message.chat.id, telegram_config.IS_RESIDENT, reply_markup=markup_resident)

@bot.message_handler(commands=['standard'])
def standard(message):
    bot.send_message(message.chat.id, telegram_config.STANDARD_MESSAGE)

@bot.message_handler(commands=['get_standard'])
def get_standard(message):
    bot.send_message(message.chat.id, telegram_config.GET_STANDARD_MESSAGE)

@bot.message_handler(commands=['property'])
def property(message):
    bot.send_message(message.chat.id, telegram_config.PROPERTY_MESSAGE)

@bot.message_handler(commands=['get_property'])
def get_property(message):
    bot.send_message(message.chat.id, telegram_config.GET_PROPERTY_MESSAGE)

@bot.message_handler(commands=['investment'])
def investment(message):
    bot.send_message(message.chat.id, telegram_config.INVESTMENT_MESSAGE)

@bot.message_handler(commands=['get_investment_type_A'])
def investment_type_A(message):
    bot.send_message(message.chat.id, telegram_config.INVESTMENT_MESSAGE_A)

@bot.message_handler(commands=['social'])
def instruction(message):
    bot.send_message(message.chat.id, telegram_config.SOCIAL_MESSAGE_1)
    bot.send_message(message.chat.id, telegram_config.SOCIAL_MESSAGE_2)

@bot.message_handler(commands=['get_social'])
def get_social(message):
    bot.send_message(message.chat.id, telegram_config.GET_SOCIAL_MESSAGE)




@bot.message_handler(commands=['calculate'])
def calculate_info(message):
    bot.register_next_step_handler(message, get_last_income)
    bot.send_message(message.chat.id, '''📌 Введи свой доход за прошлый год: ''')

def get_last_income(message):
    if not re.match(r'\d+$', message.text):
        bot.send_message(message.chat.id, '''Ошибка ввода. Необходимо ввести свой доход за прошлый год в формате: *Доход*''')
        bot.register_next_step_handler(message, get_last_income)
    else:
        global last_income
        last_income = int(message.text)
        bot.send_message(message.chat.id, '''📌 Какой вычет хотите вернуть? ''')
        markup_calculate = types.InlineKeyboardMarkup(row_width=3)
        social_button = types.InlineKeyboardButton("Социальный", callback_data='calculate_social')
        invest_button = types.InlineKeyboardButton("Инвестиционный", callback_data='calculate_invest')
        property_button = types.InlineKeyboardButton("Имущественный", callback_data='calculate_property')
        markup_calculate.add(social_button, invest_button, property_button)
        bot.send_message(message.chat.id, '''Виды налоговых вычетов: ''', reply_markup=markup_calculate)

@bot.callback_query_handler(func=lambda call: call.data.startswith('test'))
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'test_resident':
                markup_answer = types.InlineKeyboardMarkup(row_width=1)
                ans_button = types.InlineKeyboardButton("Да", callback_data='1')
                markup_answer.add(ans_button)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=telegram_config.IS_RESIDENT,
                reply_markup=markup_answer)
                markup_income = types.InlineKeyboardMarkup(row_width=2)
                yes_button = types.InlineKeyboardButton("Да", callback_data='test_has_income')
                no_button = types.InlineKeyboardButton("Нет", callback_data='test_not_income')
                markup_income.add(yes_button, no_button)
                bot.send_message(call.message.chat.id, telegram_config.INCOME_MESSAGE, reply_markup=markup_income)
            elif call.data == 'test_not_resident':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=telegram_config.IS_RESIDENT + '❌',
                reply_markup=None)
                markup_restart = types.InlineKeyboardMarkup(row_width=1)
                restart_button = types.InlineKeyboardButton("Повторить тест", callback_data='test_restart_1')
                markup_restart.add(restart_button)
                bot.send_message(call.message.chat.id, telegram_config.REJECT_MESSAGE_1, reply_markup=markup_restart)
            elif call.data == 'test_has_income':
                bot.send_message(call.message.chat.id, 'Да')
                bot.send_message(call.message.chat.id, telegram_config.REFUND_MESSAGE_INFO)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=telegram_config.INCOME_MESSAGE,
                reply_markup=None)
            elif call.data == 'test_not_income':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=telegram_config.INCOME_MESSAGE + '❌',
                reply_markup=None)
                markup_restart = types.InlineKeyboardMarkup(row_width=1)
                restart_button = types.InlineKeyboardButton("Повторить тест", callback_data='test_restart_2')
                markup_restart.add(restart_button)
                bot.send_message(call.message.chat.id, telegram_config.REJECT_MESSAGE_2, reply_markup=markup_restart)
            elif call.data == 'test_restart_1':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=telegram_config.REJECT_MESSAGE_1,
                reply_markup=None)
                markup_resident = types.InlineKeyboardMarkup(row_width=2)
                yes_button = types.InlineKeyboardButton("Да", callback_data='test_resident')
                no_button = types.InlineKeyboardButton("Нет", callback_data='test_not_resident')
                markup_resident.add(yes_button, no_button)
                bot.send_message(call.message.chat.id, telegram_config.IS_RESIDENT, reply_markup=markup_resident)
            elif call.data == 'test_restart_2':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=telegram_config.REJECT_MESSAGE_2,
                reply_markup=None)
                markup_resident = types.InlineKeyboardMarkup(row_width=2)
                yes_button = types.InlineKeyboardButton("Да", callback_data='test_resident')
                no_button = types.InlineKeyboardButton("Нет", callback_data='test_not_resident')
                markup_resident.add(yes_button, no_button)
                bot.send_message(call.message.chat.id, telegram_config.IS_RESIDENT, reply_markup=markup_resident)
    except Exception as e:
        print(repr(e))
    return True

@bot.callback_query_handler(func=lambda call: call.data.startswith('calculate'))
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'calculate_social':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''Расчет социальных вычетов
                ''', reply_markup=None)
                markup_calculate_social = types.InlineKeyboardMarkup(row_width=2)
                charity_button = types.InlineKeyboardButton("На благотворительность", callback_data='social_charity')
                education_button = types.InlineKeyboardButton("На обучение", callback_data='social_education')
                medicine_button = types.InlineKeyboardButton("На лечение и лекарства", callback_data='social_medicine')
                insurance_button = types.InlineKeyboardButton("На страхование", callback_data='social_insurance')
                qualification_button = types.InlineKeyboardButton("На независимую оценку квалификации", callback_data='social_qualification')
                markup_calculate_social.add(charity_button, education_button, medicine_button, insurance_button, qualification_button)
                bot.send_message(call.message.chat.id, '''📌 Какой вид социального вычета у тебя?''', reply_markup=markup_calculate_social)
            elif call.data == 'calculate_invest':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''Расчет инвестиционных вычетов''',
                reply_markup=None)
                markup_calculate_invest = types.InlineKeyboardMarkup(row_width=2)
                type_a_button = types.InlineKeyboardButton("Льгота типа А", callback_data='invest_a')
                type_b_button = types.InlineKeyboardButton("Льгота типа Б", callback_data='invest_b')
                markup_calculate_invest.add(type_a_button, type_b_button)
                bot.send_message(call.message.chat.id, '''📌 Какой тип льгот по ИИС у тебя? ''', reply_markup=markup_calculate_invest)
            elif call.data == 'calculate_property':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''Расчет имущественных вычетов''',
                reply_markup=None)
                bot.send_message(call.message.chat.id, '''📌Введи стоимость приобретенного или проданного жилья''')
                bot.register_next_step_handler(call.message, get_property_cost)
    except Exception as e:
        print(repr(e))
    return True

@bot.callback_query_handler(func=lambda call: call.data.startswith('social'))
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'social_charity':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌 Какой вид социального вычета у тебя?''',
                reply_markup=None)
                bot.send_message(call.message.chat.id, '''📌 Сколько ты отдал на благотворительность в этом году? ''')
                bot.register_next_step_handler(call.message, get_last_charity)
            if call.data == 'social_education':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌 Какой вид социального вычета у тебя?''',
                reply_markup=None)
                markup_education = types.InlineKeyboardMarkup(row_width=2)
                own_button = types.InlineKeyboardButton("Свое обучение", callback_data='social_education_own')
                child_button = types.InlineKeyboardButton("На обучение своего ребенка(подпечённого)", callback_data='social_education_child')
                markup_education.add(own_button, child_button)
                bot.send_message(call.message.chat.id, '''📌 Ты платил за себя или за своего ребенка(подпечённого)?''', reply_markup=markup_education)
            if call.data == 'social_medicine':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌 Какой вид социального вычета у тебя?''',
                reply_markup=None)
                bot.send_message(call.message.chat.id, '''Введи стоимость медицинских услуг и/или лекарств:''')
                bot.register_next_step_handler(call.message, get_last_cost)
            if call.data == 'social_insurance':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌 Какой вид социального вычета у тебя?''',
                reply_markup=None)
                bot.send_message(call.message.chat.id, '''📌 Сколько ты заплатил за страховку в этом году?''')
                bot.register_next_step_handler(call.message, get_last_cost)
            if call.data == 'social_qualification':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌 Какой вид социального вычета у тебя?''',
                reply_markup=None)
                bot.send_message(call.message.chat.id, '''📌 Сколько ты заплатил за независимую оценку квалификации в этом году?''')
                bot.register_next_step_handler(call.message, get_last_cost)
            if call.data == 'social_education_own':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌 Ты платил за себя или за своего ребенка(подпечённого)? ''',
                reply_markup=None)
                bot.send_message(call.message.chat.id, '''Введи стоимость обучения:''')
                bot.register_next_step_handler(call.message, get_last_cost)
            if call.data == 'social_education_child':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌 Ты платил за себя или за своего ребенка(подпечённого)? ''',
                reply_markup=None)
                bot.send_message(call.message.chat.id, '''Введи стоимость обучения:''')
                bot.register_next_step_handler(call.message, get_child_education_price)
        
    except Exception as e:
        print(repr(e))
    return True

def get_last_charity(message):
    if not re.match(r'\d+$', message.text):
        bot.send_message(message.chat.id, '''Ошибка ввода. Необходимо ввести количество потраченных денег в формате: *Сумма*''')
        bot.register_next_step_handler(message, get_last_charity)
    else:
        global last_income
        last_charity = int(message.text)
        final_income = 0.0325*last_income
        final_charity = 0.13*last_charity
        if final_income > final_charity:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_charity)}''')
        else:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_income)}''')

def get_last_cost(message):
    if not re.match(r'\d+$', message.text):
        bot.send_message(message.chat.id, '''Ошибка ввода. Необходимо ввести количество потраченных денег в формате: *Сумма*''')
        bot.register_next_step_handler(message, get_last_cost)
    else:
        global last_income
        last_cost = int(message.text)
        final_income = 0.13*last_income
        final_cost = 0.13*last_cost
        if final_income > final_cost and final_cost < 15600:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_cost)}''')
        elif final_income <= final_cost and final_income < 15600:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_income)}''')
        else:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: 15600''')

def get_child_education_price(message):
    if not re.match(r'\d+$', message.text):
        bot.send_message(message.chat.id, '''Ошибка ввода. Необходимо ввести количество потраченных денег в формате: *Сумма*''')
        bot.register_next_step_handler(message, get_child_education_price)
    else:
        global last_income
        last_education = int(message.text)
        final_income = 0.13*last_income
        final_education = 0.13*last_education
        if final_income > final_education and final_education < 6500:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_education)}''')
        elif final_income <= final_education and final_income < 6500:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_income)}''')
        else:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {6500}''')

@bot.callback_query_handler(func=lambda call: call.data.startswith('invest'))
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'invest_a':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌 Какой тип льгот по ИИС у тебя?
                ''', reply_markup=None)
                bot.send_message(call.message.chat.id, '''📌 Сколько лет у тебя открыт ИИС (максимум 3 года)? ''')
                bot.register_next_step_handler(call.message, get_duration_invest_a)
            elif call.data == 'invest_b':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌 Какой тип льгот по ИИС у тебя?''',
                reply_markup=None)
                bot.send_message(call.message.chat.id, '''📌 Введи размер дохода, полученного за 3 года с ИИС (например, 1000,2000,3000)''')
                bot.register_next_step_handler(call.message, get_invest_b)
    except Exception as e:
        print(repr(e))
    return True

def get_invest_b(message):
    if not re.match(r'\d+,\d+,\d+$', message.text):
        bot.send_message(message.chat.id, '''Ошибка ввода. Необходимо ввести размер дохода, полученного за 3 года с ИИС в формате: *Доход за первый год*,*Доход за второй год*,*Доход за третий год*''')
        bot.register_next_step_handler(message, get_invest_b)
    else:
        incomes = message.text.split(',')
        bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(sum([int(x) for x in incomes])*0.13)}''')

def get_duration_invest_a(message):
    if not re.match(r'\d+$', message.text) or int(message.text) < 1:
        bot.send_message(message.chat.id, '''Ошибка ввода. Необходимо ввести количество лет, в течение которых у тебя открыт ИИС в формате: *Количество лет*''')
        bot.register_next_step_handler(message, get_duration_invest_a)
    else:
        global invest_duration
        invest_duration = 3 if int(message.text) > 3 else int(message.text)
        bot.send_message(message.chat.id, '''📌 Введи размеры взносов на ИСС (например, 1000,2000,3000)''')
        bot.register_next_step_handler(message, get_invest_a)

def get_invest_a(message):
    global invest_duration
    if not re.match(r'^\d+(?:,\d+){0,2}$', message.text) or message.text.count(',') != invest_duration - 1:
        bot.send_message(message.chat.id, '''Ошибка ввода. Необходимо ввести размеры взносов за указанное количество лет с ИИС в формате: *Взнос за первый год*,*Взнос за второй год*,*Взнос за третий год*''')
        bot.register_next_step_handler(message, get_invest_a)
    else:
        incomes = message.text.split(',')
        global last_income
        final_income = 0.13*last_income
        total_invest = 0
        for i in range(invest_duration):
            final_invest = 0.13*int(incomes[i])
            if final_income > final_invest and final_invest < 52000:
                total_invest += final_invest
            elif final_income <= final_invest and final_income < 52000:
                total_invest += final_income
            else:
                total_invest += 52000
        bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(total_invest)}''')

@bot.callback_query_handler(func=lambda call: call.data.startswith('invest'))
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'invest_a':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌 Какой тип льгот по ИИС у тебя?
                ''', reply_markup=None)
                bot.send_message(call.message.chat.id, '''📌 Сколько лет у тебя открыт ИИС (максимум 3 года)? ''')
                bot.register_next_step_handler(call.message, get_duration_invest_a)
            elif call.data == 'invest_b':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌 Какой тип льгот по ИИС у тебя?''',
                reply_markup=None)
                bot.send_message(call.message.chat.id, '''📌 Введи размер дохода, полученного за 3 года с ИИС (например, 1000,2000,3000)''')
                bot.register_next_step_handler(call.message, get_invest_b)
    except Exception as e:
        print(repr(e))
    return True

def get_property_cost(message):
    if not re.match(r'\d+$', message.text):
        bot.send_message(message.chat.id, '''Ошибка ввода. Необходимо ввести стоимость жилья в формате: *Стоимость жилья*''')
        bot.register_next_step_handler(message, get_property_cost)
    else:
        global property_cost
        property_cost = int(message.text)
        markup_property = types.InlineKeyboardMarkup(row_width=2)
        prev_button = types.InlineKeyboardButton(f'{datetime.now().year - 1}', callback_data='property_prev_year')
        prev_prev_button = types.InlineKeyboardButton(f'{datetime.now().year - 2}', callback_data='property_prev_prev_year')
        prev_prev_prev_button = types.InlineKeyboardButton(f'{datetime.now().year - 3}', callback_data='property_prev_prev_prev_year')
        markup_property.add(prev_button, prev_prev_button, prev_prev_prev_button)
        bot.send_message(message.chat.id, '''📌В каком году ты купил квартиру? ''', reply_markup=markup_property)

@bot.callback_query_handler(func=lambda call: call.data.startswith('property'))
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'property_prev_year':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌В каком году ты купил квартиру? 
                ''', reply_markup=None)
                global last_income
                global property_cost
                final_income = 0.13*last_income
                final_property = 0.13*property_cost
                if final_income > final_property and final_property < 260000:
                    bot.send_message(call.message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_property)}''')
                elif final_income <= final_property and final_income < 260000:
                    bot.send_message(call.message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_income)}''')
                else:
                    bot.send_message(call.message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {260000}''')
            elif call.data == 'property_prev_prev_year':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌В каком году ты купил квартиру? ''',
                reply_markup=None)
                bot.send_message(call.message.chat.id, f'''📌 Введи свой доход за {datetime.now().year - 2} год: ''')
                bot.register_next_step_handler(call.message, get_prev_prev_income)
            elif call.data == 'property_prev_prev_prev_year':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''📌В каком году ты купил квартиру? ''',
                reply_markup=None)
                bot.send_message(call.message.chat.id, f'''📌 Введи свой доход за {datetime.now().year - 2} и {datetime.now().year - 3} годы (например, 1000, 2000): ''')
                bot.register_next_step_handler(call.message, get_prev_prev_prev_income)
    except Exception as e:
        print(repr(e))
    return True

def get_prev_prev_income(message):
    if not re.match(r'\d+$', message.text):
        bot.send_message(message.chat.id, f'''Ошибка ввода. Необходимо ввести свой доход за {datetime.now().year - 2} год в формате: *Доход*''')
        bot.register_next_step_handler(message, get_prev_prev_income)
    else:
        global last_income
        global property_cost
        final_property = 0.13*property_cost
        final_income = 0.13*(last_income + int(message.text))
        if final_income > final_property and final_property < 260000:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_property)}''')
        elif final_income <= final_property and final_income < 260000:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_income)}''')
        else:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {260000}''')

def get_prev_prev_prev_income(message):
    if not re.match(r'\d+,\d+$', message.text):
        bot.send_message(message.chat.id, f'''Ошибка ввода. Необходимо ввести свой доход за {datetime.now().year - 2} год в формате: *Доход за {datetime.now().year - 2} год*,*Доход за {datetime.now().year - 3} год*''')
        bot.register_next_step_handler(message, get_prev_prev_prev_income)
    else:
        global last_income
        global property_cost
        final_property = 0.13*property_cost
        incomes = message.text.split(',')
        final_income = 0.13*(sum([int(x) for x in incomes]) + last_income)
        if final_income > final_property and final_property < 260000:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_property)}''')
        elif final_income <= final_property and final_income < 260000:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {int(final_income)}''')
        else:
            bot.send_message(message.chat.id, f'''Размер вычета, на который ты можешь претендовать: {260000}''')



@bot.message_handler(content_types=['text'])
def undefined_input(message):
    bot.send_message(message.chat.id, telegram_config.IDK)

# RUN
bot.polling(none_stop=True)
