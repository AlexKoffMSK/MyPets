import telebot
from telebot import types
from datetime import date
import dataframe_image as dfi
from config import token
from functions import *

date_to_parse=[]
today = date.today()
is_leap_year = False

bot = telebot.TeleBot(token)

def print_welcome(chat_id, from_user):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Ввести дату для запроса")
    button2 = types.KeyboardButton("Информация о боте")
    markup.add(button1, button2)
    bot.send_message(chat_id,
    "Привет, {0.first_name}! Я умею доставать курсы валют, установленные Центральным банком РФ на заданную дату между 01.07.1992 и сегодняшним днём!"
    .format(from_user), reply_markup=markup)

#Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print_welcome(message.chat.id, message.from_user)

@bot.message_handler(content_types=['text'])
def processing_users_response_to_welcome_message_by_bot(user_message):
    if user_message.text == 'Ввести дату для запроса':
        bot_msg = bot.send_message(user_message.chat.id, 'Введите год в формате ГГГГ (1992, 2003 и т.д.): ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_year)
    elif user_message.text == 'Информация о боте':
        bot.send_message(user_message.chat.id,
            'Привет! Я Алексей Рожков, это мой первый бот в телеграм. Он работает так: Вы задаете желаемую дату, а бот получает информацию о курсах валют с сайта Центрального банка РФ на указанную дату и присылает Вам в чат.')
    else:
        bot_msg = bot.send_message(user_message.chat.id, 'Неожидаемый запрос: ' + user_message.text)
        bot.register_next_step_handler(bot_msg, send_welcome)

@bot.message_handler(content_types=['text'])
def process_users_response_by_bot_request_to_insert_year(user_message):
    date_to_parse.clear()
    global is_leap_year
    is_leap_year = False
    if int(user_message.text) < 1992 or int(user_message.text) > int(today.year):
        bot_msg = bot.send_message(user_message.chat.id, 'Вы ввели некорректный год! Введите правильно!')
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_year)
    else:
        date_to_parse.append(user_message.text)
        if (int(user_message.text) % 4) == 0:
            is_leap_year = True
        bot_msg = bot.send_message(user_message.chat.id, 'Введите месяц в формате ММ (02, 08, 11 и т.д.): ',reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_month)

@bot.message_handler(content_types=['text'])
def process_users_response_by_bot_request_to_insert_month(user_message):
    if int(user_message.text) > 12:
        bot_msg = bot.send_message(user_message.chat.id,'Введен некорректный месяц! Введите правильно!')
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_month)
    else:
        date_to_parse.append(user_message.text)
        bot_msg = bot.send_message(user_message.chat.id, 'Введите день в формате ДД (01, 08, 29 и т.д.): ')
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_day)

@bot.message_handler(content_types=['text'])
def process_users_response_by_bot_request_to_insert_day(user_message):
    if int(user_message.text) < 1 or int(user_message.text) > 31:
        bot_msg = bot.send_message(user_message.chat.id, 'Введен некорректный день ( <1, >31) ! Введите правильно!')
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_day)
    elif int(date_to_parse[1]) == 2 and is_leap_year == False and int(user_message.text) > 28:
        bot_msg = bot.send_message(user_message.chat.id, 'Введен некорректный день (Невисокосный год, >28)! Введите правильно!')
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_day)
    elif int(date_to_parse[1]) == 2 and is_leap_year == True and int(user_message.text) > 29:
        bot_msg = bot.send_message(user_message.chat.id,'Введен некорректный день (Високосный год, > 29)! Введите правильно!')
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_day)
    elif (int(date_to_parse[1]) == 4 or int(date_to_parse[1]) == 6 or int(date_to_parse[1]) == 9 or int(date_to_parse[1]) == 11) and (int(user_message.text) == 31):
        bot_msg = bot.send_message(user_message.chat.id,'Введен некорректный день (В месяце 30 дней, 31)! Введите правильно!')
        bot.register_next_step_handler(bot_msg, process_users_response_by_bot_request_to_insert_day)
    else:
        date_to_parse.append(user_message.text)
        bot_msg = bot.send_message(user_message.chat.id, 'Выбранная дата для поиска курса валюты: ' + date_to_parse[2] + '.' + date_to_parse[1] + '.'+ date_to_parse[0])
        parse_day_to_get_data(bot_msg)

@bot.message_handler(content_types=['text'])
def parse_day_to_get_data(user_message):
    day_soup = GetBSSourceDataFromCBRFByDate(date_to_parse[2], date_to_parse[1], date_to_parse[0])
    data_frame = MakeDataFrameFromCurLink(day_soup)

    #Так как Яндекс.Облако не делает файл png и, соответственно, не отправляет его в телеграм (а я еще не разобрался - что не так),
    #то пока что фукнции убраны, а данные преобразуем в текст и посылаем пользователю. Тоже работает!
    # dfi.export(data_frame, 'data.png')
    # bot.send_photo(user_message.chat.id, open('data.png', 'rb'))

    bot.send_message(user_message.chat.id, data_frame.to_string())

    send_welcome(user_message)

    #хорошо бы доделать выбор - валюту по выбору либо все за день

bot.infinity_polling()