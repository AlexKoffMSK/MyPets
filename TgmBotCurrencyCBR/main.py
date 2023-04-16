import telebot
from telebot import types
from datetime import date
import dataframe_image as dfi
from config import token
from functions import *

date_to_parse=[]
today = date.today()

bot = telebot.TeleBot(token)

def print_welcome(chat_id, from_user):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Ввести дату для запроса")
    button2 = types.KeyboardButton("Рассказать о боте")
    markup.add(button1, button2)
    bot.send_message(chat_id,
    "Привет, {0.first_name}! я умею доставать курс нужной валюты, установленный Центральный банком РФ на заданную дату между 01.07.1992 и сегодняшним днём!"
    .format(from_user), reply_markup=markup)

#Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print_welcome(message.chat.id, message.from_user)

@bot.message_handler(content_types=['text'])
def processing_users_response_to_welcome_message_by_bot(user_message):
    if user_message.text == 'Ввести дату для запроса':
        year = bot.send_message(user_message.chat.id, 'Введите год в формате ГГГГ: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(year, process_users_response_by_bot_request_to_insert_year)
    elif user_message.text == 'Рассказать о боте':
        bot.send_message(user_message.chat.id,
            'Вы задаете дату и выбираете валюту, а бот получает информацию с сайта Центрального банка РФ по соответствующему запросу.')
    else:
        bot_msg = bot.send_message(user_message.chat.id, 'Неожидаемый запрос: ' + user_message.text)
        bot.register_next_step_handler(bot_msg, send_welcome)

@bot.message_handler(content_types=['text'])
def process_users_response_by_bot_request_to_insert_year(user_message):
    date_to_parse.clear()
    if int(user_message.text) < 1992 or int(user_message.text) > int(today.year):
        bot_msg = bot.send_message(user_message.chat.id, 'Вы ввели некорректный год! Введите правильно!')
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_year)
    else:
        date_to_parse.append(user_message.text)
        bot_msg = bot.send_message(user_message.chat.id, 'Введите месяц в формате ММ: ',reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_month)

@bot.message_handler(content_types=['text'])
def process_users_response_by_bot_request_to_insert_month(user_message):
    if int(user_message.text) > 12:
        bot_msg = bot.send_message(user_message.chat.id,'Введен некорректный месяц! Введите правильно!')
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_month)
    else:
        date_to_parse.append(user_message.text)
        bot_msg = bot.send_message(user_message.chat.id, 'Введите день в формате ДД: ')
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_day)

@bot.message_handler(content_types=['text'])
def process_users_response_by_bot_request_to_insert_day(user_message):
    if int(user_message.text) <= 0 or int(user_message.text) > 31:
        #прописать ограничения по високосному году и количеству дней в месяцах
        bot_msg = bot.send_message(user_message.chat.id,'Введен некорректный день! Введите правильно!')
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_day)
    else:
        date_to_parse.append(user_message.text)
        bot_msg = bot.send_message(user_message.chat.id, 'Выбранная дата для поиска курса валюты: ' + date_to_parse[2] + '.' + date_to_parse[1] + '.'+ date_to_parse[0])
        parse_day_to_get_data(bot_msg)

@bot.message_handler(content_types=['text'])
def parse_day_to_get_data(user_message):
    day_soup = GetBSSourceDataFromCBRFByDate(date_to_parse[2], date_to_parse[1], date_to_parse[0])
    data_frame = MakeDataFrameFromCurLink(day_soup)
    dfi.export(data_frame, 'data.png')
    bot.send_photo(user_message.chat.id, open('data.png', 'rb'))
    send_welcome(user_message)

bot.infinity_polling()