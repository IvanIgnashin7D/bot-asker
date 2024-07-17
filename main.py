from telebot import *
from types import *
import sqlite3
from dotenv import load_dotenv
import os


load_dotenv()
token = os.getenv('BOT_TOKEN')
bot = TeleBot(token=token)
BAZA = os.getenv('BAZA')

conn = sqlite3.connect(BAZA)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (id int primary key, name TEXT, age int, answers TEXT)')
conn.commit()
cur.close()
conn.close()

questions = ['Вопрос 1/10 \nЧто из перечисленного для вас является самым увлекательным зимним занятием?',
             'Вопрос 2/10 \nКакое ваше любимое зимнее блюдо?',
             'Вопрос 3/10 \nКак вы предпочитаете проводить холодные зимние вечера?',
             'Вопрос 4/10 \nКакое ваше предпочтение в отношении новогодних праздников?',
             'Вопрос 5/10 \nКакие зимние украшения вам больше нравятся?',
             'Вопрос 6/10 \nЧто для вас является самым красивым зимним пейзажем?',
             'Вопрос 7/10 \nКакую зимнюю одежду предпочитаете?',
             'Вопрос 8/10 \nКак вы относитесь к зимним путешествиям?',
             'Вопрос 9/10 \nКакой ваш любимый зимний праздник?',
             'Вопрос 10/10 \nКакой фильм озимних каникулах вы предпочитаете:']
answers = [['Катание на лыжах', 'Катание на сноуборде', 'Коньки', 'Снежки'],
           ['Горячий шоколад с зефиром', 'Тёплый суп', 'Пирог с ягодами', 'Блины'],
           ['За чтением книг у камина', 'Смотря кино', 'Играя в настольные игры', 'Собирая пазлы'],
           ['Праздновать дома в уютной обстановке', 'Отдыхать в путешествии', 'Устривать вечеринку с друзьями', 'Посещать новогодние мероприятия'],
           ['Гирлянды  и огоньки', 'Снежинки и снеговики', 'Елочные украшения', 'Новогодние фонарики'],
           ['Заснеженные горы', 'Лес в сегу', 'Каток с заснеженными елями', 'Домик в лесу с гирляндами'],
           ['Пуховик', 'Шерстяное пальто', 'Уютный свитер', 'Теплый шарф и варежки'],
           ['Люблю кататься на лыжах и сноуборде', 'Предпочитаю уютные горнолыжные курорты', 'Предпочитаю путешествия в теплые страны зимой', 'Cчитаю, что зима - лучшее время для путешествий'],
           ['Новый год', 'Рождество', 'День святого валентина', 'Масленица'],
           ['Один дома', 'Хроники Нарнии: Лев, Ведьма и Шкаф', 'Мастер и маргарита', 'Ледниковый период']]

user_answers = ''
sent = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_answers = ''
    sent = bot.send_message(message.chat.id, text='Введите ваш возраст, пожалуйста')
    bot.register_next_step_handler(sent, starting_test)
def starting_test(message):
    try:
        conn = sqlite3.connect(BAZA)
        cur = conn.cursor()
        cur.execute('INSERT INTO users (id, name, age) VALUES (?, ?, ?)', (message.chat.id, message.from_user.first_name, message.text))
        conn.commit()
        cur.close()
        conn.close()
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Начать опрос!', callback_data='начать опрос'))
        sent[message.chat.id] = bot.send_message(message.chat.id, text='Спасибо!', reply_markup=keyboard)
    except:
        cur.close()
        conn.close()
        keybard = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text='Да', callback_data='да')
        btn2 = types.InlineKeyboardButton(text='Нет', callback_data='нет')
        keybard.add(btn1, btn2)
        sent[message.chat.id] = bot.send_message(message.chat.id, text='Вы уже прошли опрос. Желаете перепройти? (прошлый результат будет удалён!)', reply_markup=keybard)


@bot.callback_query_handler(func=lambda call: call.data == 'нет')
def cancel(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=sent[call.message.chat.id].message_id, text='Отменено')


@bot.callback_query_handler(func=lambda call: call.data in ['начать опрос', 'да'])
def q1(call):
    if call.data == 'да':
        conn = sqlite3.connect(BAZA)
        cur = conn.cursor()
        cur.execute('UPDATE users SET answers = ? WHERE id = ?', (None, call.message.chat.id))
        conn.commit()
        cur.close()
        conn.close()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=answers[0][0], callback_data='вопрос 2.0')
    btn2 = types.InlineKeyboardButton(text=answers[0][1], callback_data='вопрос 2.1')
    btn3 = types.InlineKeyboardButton(text=answers[0][2], callback_data='вопрос 2.2')
    btn4 = types.InlineKeyboardButton(text=answers[0][3], callback_data='вопрос 2.3')
    keyboard.add(btn1, btn2, btn3, btn4)
    sent[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=sent[call.message.chat.id].message_id,
                                                       text=questions[0], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['вопрос 2.0', 'вопрос 2.1', 'вопрос 2.2', 'вопрос 2.3'])
def q2(call):
    global user_answers
    user_answers = user_answers + '  \n1.' + answers[0][int(call.data[-1])]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=answers[1][0], callback_data='вопрос 3.0')
    btn2 = types.InlineKeyboardButton(text=answers[1][1], callback_data='вопрос 3.1')
    btn3 = types.InlineKeyboardButton(text=answers[1][2], callback_data='вопрос 3.2')
    btn4 = types.InlineKeyboardButton(text=answers[1][3], callback_data='вопрос 3.3')
    keyboard.add(btn1, btn2, btn3, btn4)
    sent[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id, message_id=sent[call.message.chat.id].message_id, text=questions[1], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['вопрос 3.0', 'вопрос 3.1', 'вопрос 3.2', 'вопрос 3.3'])
def q3(call):
    global user_answers
    user_answers = user_answers + '  \n2.' + answers[1][int(call.data[-1])]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=answers[2][0], callback_data='вопрос 4.0')
    btn2 = types.InlineKeyboardButton(text=answers[2][1], callback_data='вопрос 4.1')
    btn3 = types.InlineKeyboardButton(text=answers[2][2], callback_data='вопрос 4.2')
    btn4 = types.InlineKeyboardButton(text=answers[2][3], callback_data='вопрос 4.3')
    keyboard.add(btn1, btn2, btn3, btn4)
    sent[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=sent[call.message.chat.id].message_id,
                                                       text=questions[2], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['вопрос 4.0', 'вопрос 4.1', 'вопрос 4.2', 'вопрос 4.3'])
def q4(call):
    global user_answers
    user_answers = user_answers + '  \n3.' + answers[2][int(call.data[-1])]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=answers[3][0], callback_data='вопрос 5.0')
    btn2 = types.InlineKeyboardButton(text=answers[3][1], callback_data='вопрос 5.1')
    btn3 = types.InlineKeyboardButton(text=answers[3][2], callback_data='вопрос 5.2')
    btn4 = types.InlineKeyboardButton(text=answers[3][3], callback_data='вопрос 5.3')
    keyboard.add(btn1, btn2, btn3, btn4)
    sent[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=sent[call.message.chat.id].message_id,
                                                       text=questions[3], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['вопрос 5.0', 'вопрос 5.1', 'вопрос 5.2', 'вопрос 5.3'])
def q5(call):
    global user_answers
    user_answers = user_answers + '  \n4.' + answers[3][int(call.data[-1])]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=answers[4][0], callback_data='вопрос 6.0')
    btn2 = types.InlineKeyboardButton(text=answers[4][1], callback_data='вопрос 6.1')
    btn3 = types.InlineKeyboardButton(text=answers[4][2], callback_data='вопрос 6.2')
    btn4 = types.InlineKeyboardButton(text=answers[4][3], callback_data='вопрос 6.3')
    keyboard.add(btn1, btn2, btn3, btn4)
    sent[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=sent[call.message.chat.id].message_id,
                                                       text=questions[4], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['вопрос 6.0', 'вопрос 6.1', 'вопрос 6.2', 'вопрос 6.3'])
def q6(call):
    global user_answers
    user_answers = user_answers + '  \n5.' + answers[4][int(call.data[-1])]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=answers[5][0], callback_data='вопрос 7.0')
    btn2 = types.InlineKeyboardButton(text=answers[5][1], callback_data='вопрос 7.1')
    btn3 = types.InlineKeyboardButton(text=answers[5][2], callback_data='вопрос 7.2')
    btn4 = types.InlineKeyboardButton(text=answers[5][3], callback_data='вопрос 7.3')
    keyboard.add(btn1, btn2, btn3, btn4)
    sent[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=sent[call.message.chat.id].message_id,
                                                       text=questions[5], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['вопрос 7.0', 'вопрос 7.1', 'вопрос 7.2', 'вопрос 7.3'])
def q7(call):
    global user_answers
    user_answers = user_answers + '  \n6.' + answers[5][int(call.data[-1])]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=answers[6][0], callback_data='вопрос 8.0')
    btn2 = types.InlineKeyboardButton(text=answers[6][1], callback_data='вопрос 8.1')
    btn3 = types.InlineKeyboardButton(text=answers[6][2], callback_data='вопрос 8.2')
    btn4 = types.InlineKeyboardButton(text=answers[6][3], callback_data='вопрос 8.3')
    keyboard.add(btn1, btn2, btn3, btn4)
    sent[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=sent[call.message.chat.id].message_id,
                                                       text=questions[6], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['вопрос 8.0', 'вопрос 8.1', 'вопрос 8.2', 'вопрос 8.3'])
def q8(call):
    global user_answers
    user_answers = user_answers + '  \n7.' + answers[6][int(call.data[-1])]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=answers[7][0], callback_data='вопрос 9.0')
    btn2 = types.InlineKeyboardButton(text=answers[7][1], callback_data='вопрос 9.1')
    btn3 = types.InlineKeyboardButton(text=answers[7][2], callback_data='вопрос 9.2')
    btn4 = types.InlineKeyboardButton(text=answers[7][3], callback_data='вопрос 9.3')
    keyboard.add(btn1, btn2, btn3, btn4)
    sent[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=sent[call.message.chat.id].message_id,
                                                       text=questions[7], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['вопрос 9.0', 'вопрос 9.1', 'вопрос 9.2', 'вопрос 9.3'])
def q9(call):
    global user_answers
    user_answers = user_answers + '  \n8.' + answers[7][int(call.data[-1])]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=answers[8][0], callback_data='вопрос 10.0')
    btn2 = types.InlineKeyboardButton(text=answers[8][1], callback_data='вопрос 10.1')
    btn3 = types.InlineKeyboardButton(text=answers[8][2], callback_data='вопрос 10.2')
    btn4 = types.InlineKeyboardButton(text=answers[8][3], callback_data='вопрос 10.3')
    keyboard.add(btn1, btn2, btn3, btn4)
    sent[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=sent[call.message.chat.id].message_id,
                                                       text=questions[8], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['вопрос 10.0', 'вопрос 10.1', 'вопрос 10.2', 'вопрос 10.3'])
def q10(call):
    global user_answers
    user_answers = user_answers + '  \n9.' + answers[8][int(call.data[-1])]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=answers[9][0], callback_data='0')
    btn2 = types.InlineKeyboardButton(text=answers[9][1], callback_data='1')
    btn3 = types.InlineKeyboardButton(text=answers[9][2], callback_data='2')
    btn4 = types.InlineKeyboardButton(text=answers[9][3], callback_data='3')
    keyboard.add(btn1, btn2, btn3, btn4)
    sent[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=sent[call.message.chat.id].message_id,
                                                       text=questions[9], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['0', '1', '2', '3'])
def end(call):
    global user_answers
    user_answers = user_answers + '  \n10. ' + answers[9][int(call.data[-1])]
    user_answers = user_answers[2:]
    sent[call.message.chat.id] = bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=sent[call.message.chat.id].message_id,
                                                       text='Опрос заверешён')
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
    cur.execute('UPDATE users SET answers = ? WHERE id = ?', (user_answers, call.message.chat.id))
    conn.commit()
    cur.close()
    conn.close()


@bot.message_handler(func=lambda message: message.text == 'info')
@bot.message_handler(commands=['info'])
def info(message):
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    for i in users:
        bot.send_message(message.chat.id, text=f'Ответы пользователя {i[1]} (возраст - {i[2]}): \n{i[3]}')


bot.polling()