# -*- coding: utf-8 -*-
from decimal import *
import telebot
import datetime
from telebot import types, apihelper
import sqlite3
import config 
import random
import time
import os
import json
from light_qiwi import *
import keyboards
import requests
from multiprocessing import Process
from datetime import datetime, timedelta

# BOT
WalletID = 'btc-e99e20b13f82944469dc9a0246ac1c3f'
transfer_key = '2VpxuhvzoUGFW2feNdwbB85yA1Sp2nUv'
arb_url = config.arb_url
chat_url = config.chat_url
help_url = config.chat_url

bot = telebot.TeleBot(config.bot_token)

@bot.message_handler(commands=['start'])
def start_message(message):
	if message.chat.type == 'private':
		userid = str(message.chat.id)
		print(message.text)
		username = str(message.from_user.username)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute('SELECT * FROM ugc_users WHERE id IS '+str(userid))
		row = q.fetchone()
		if row is None:
			now = datetime.now()
			now_date = str(str(now)[:10])
			desponse = requests.post(f'https://apirone.com/api/v2/wallet/{WalletID}/address').json()['address']
			q.execute("INSERT INTO ugc_users (id,name,btc,data_reg) VALUES ('%s', '%s', '%s', '%s')"%(userid,username,desponse,now_date))
			connection.commit()
			bot.send_message(message.chat.id,f'👑 Добро пожаловать, <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a> !\n\nМоя цель - создать безопасную торговую среду для продавца и покупателя в соответствии с моими правилами.',parse_mode='HTML',reply_markup=keyboards.main)
			if message.text[7:] != '':
				if message.text[7:] != message.chat.id:
					q.execute("update ugc_users set ref = " + str(message.text[7:])+ " where id = " + str(message.chat.id))
					connection.commit()
					q.execute("update ugc_users set ref_colvo =ref_colvo + 1 where id = " + str(message.text[7:]))
					connection.commit()
					bot.send_message(message.text[7:], f'Новый реферал! <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>',parse_mode='HTML', reply_markup=keyboards.main)
			msg = bot.send_message(message.chat.id,f'👑 Добро пожаловать, <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>',parse_mode='HTML', reply_markup=keyboards.main)
		else:
			bot.send_message(message.chat.id, f'👑 Добро пожаловать, <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a> !\n\nМоя цель - создать безопасную торговую среду для продавца и покупателя в соответствии с моими правилами.',parse_mode='HTML', reply_markup=keyboards.main)

@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.chat.type == 'private':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		username = str(message.from_user.username)
		q.execute(f"SELECT name FROM ugc_users where id = '{message.chat.id}'")
		name = q.fetchone()
		if str(name[0]) == str(username):
			pass
		else:
			q.execute(f"update ugc_users set name = '{username}' where id = '{message.chat.id}'")
			connection.commit()

		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT status FROM ugc_users where id is " + str(message.chat.id))
		status = q.fetchone()
		if str(status[0]) == str('Активен'):


			if "https://telegram.me/BTC_CHANGE_BOT?" in str(message.text):
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("INSERT INTO btcbankir (user,text) VALUES ('%s', '%s')"%(message.chat.id,message.text))
				connection.commit()
				bot.send_message(message.chat.id, '♻️ Платеж проверяется, время зачисления 1-5 минут')


			if message.text.lower() == '/admin':
				if message.chat.id == config.admin:
					msg = bot.send_message(message.chat.id, '<b>Привет, админ!</b>',parse_mode='HTML', reply_markup=keyboards.admin)

			elif message.text.lower() == 'настройки':
				if message.chat.id == config.admin:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute("SELECT com_sdelka FROM config  where id = "+str(1))
					com_sdelka = q.fetchone()[0]
					q.execute("SELECT com_vvod FROM config  where id = "+str(1))
					com_vvod = q.fetchone()[0]
					q.execute("SELECT id_arbtr FROM config  where id = "+str(1))
					id_arbtr = q.fetchone()[0]
					q.execute("SELECT com_vivod FROM config  where id = "+str(1))
					com_vivod = q.fetchone()[0]
					q.execute("SELECT uv_dep FROM config  where id = "+str(1))
					uv_dep = q.fetchone()[0]
					q.execute("SELECT uv_arb FROM config  where id = "+str(1))
					uv_arb = q.fetchone()[0]
					q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
					uv_sdelki = q.fetchone()[0]
					q.execute("SELECT uv_vivod FROM config  where id = "+str(1))
					uv_vivod = q.fetchone()[0]
					q.execute("SELECT qiwi_phone FROM config  where id = "+str(1))
					qiwi_phone = q.fetchone()
					q.execute("SELECT qiwi_token FROM config  where id = "+str(1))
					qiwi_token = q.fetchone()
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='Изменить комиссию за пополнение',callback_data=f'изменитькоммисию{1}'))
					keyboard.add(types.InlineKeyboardButton(text='Изменить комиссию за вывод',callback_data=f'изменитькоммисию{2}'))
					keyboard.add(types.InlineKeyboardButton(text='Изменить комиссию за сделки',callback_data=f'изменитькоммисию{3}'))
					keyboard.add(types.InlineKeyboardButton(text='Настроить уведомления',callback_data=f'уведомлениянастройка'))
					keyboard.add(types.InlineKeyboardButton(text='Изменить номер QIWI',callback_data='изменитьномер_'),types.InlineKeyboardButton(text='Изменить Token QIWI',callback_data='изменитьтокен_'))
					keyboard.add(types.InlineKeyboardButton(text='Добавить арбитра',callback_data=f'арбитрыудалить{1}'),types.InlineKeyboardButton(text='Удалить арбитра',callback_data=f'арбитрыудалить{2}'))
					bot.send_message(message.chat.id, f'''Комиссия пополнения: <code>{com_vvod}</code> %
	Комиссия вывод: <code>{com_vivod}</code> %
	Комиссия за сделки: <code>{com_sdelka}</code> %

	Арбитры: <code>{id_arbtr}</code>
	Номер QIWI: <code>{qiwi_phone[0]}</code>
	Токен QIWI: <code>{qiwi_token[0]}</code>''',parse_mode='HTML', reply_markup=keyboard)


			elif message.text.lower() == 'статистика':
				if message.chat.id == config.admin:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					now = datetime.now()
					now_date = str(str(now)[:10])
					all_user_count = q.execute(f'SELECT COUNT(id) FROM ugc_users').fetchone()[0]
					new_user_count = q.execute(f'SELECT COUNT(id) FROM ugc_users WHERE data_reg = "{now_date}"').fetchone()[0]
					all_buys_count = q.execute(f'SELECT COUNT(id) FROM sdelki').fetchone()[0]
					new_buys_count = q.execute(f'SELECT COUNT(id) FROM sdelki WHERE data = "{now_date}"').fetchone()[0]
					all_earn_count = q.execute(f'SELECT SUM(summa) FROM sdelki').fetchone()[0]
					
					bot.send_message(message.chat.id, f'''Статистика проекта:
		Всего пользователей: {all_user_count}
		Новых за сегодня: {new_user_count}

		Всего сделок: {all_buys_count}
		Сделок за сегодня: {new_buys_count}

		Сумма сделок: {all_earn_count}''')

			elif message.text.lower() == 'арбитражи':
				if message.chat.id == config.admin:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					keyboard = types.InlineKeyboardMarkup()
					q.execute("SELECT * FROM sdelki where status = 'Арбитраж'")
					row = q.fetchall()
					for i in row:
						keyboard.add(types.InlineKeyboardButton(text=i[0], callback_data=f'aaadddd_{i[0]}'))

					bot.send_message(message.chat.id, "Выбери нуный: ", reply_markup=keyboard)

			elif message.text.lower() == '/arb':
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute(f"SELECT id_arbtr FROM config")
				bot_ad = str(q.fetchone()[0])
				if str(bot_ad.split('\n').count(message.chat.id) >= 1):
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					keyboard = types.InlineKeyboardMarkup()
					q.execute("SELECT * FROM sdelki where status = 'Арбитраж'")
					row = q.fetchall()
					for i in row:
						keyboard.add(types.InlineKeyboardButton(text=i[0], callback_data=f'aaadddd_{i[0]}'))
					bot.send_message(message.chat.id, "Выбери нуный: ", reply_markup=keyboard)


			elif message.text.lower() == 'cделки':
				if message.chat.id == config.admin:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute(f"SELECT * FROM sdelki")
					info = q.fetchall()
					rand = random.randint(10000000,99999999999)
					keyboard = types.InlineKeyboardMarkup()
					for i in info:
						q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
						iduser_sellname = q.fetchone()[0]
						q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
						idubuyname = q.fetchone()[0]
						doc = open(f'G{rand}.txt', 'a', encoding='utf8')
						doc.write(f'''ID: #G{i[0]} | Покупатель: @{idubuyname} | Продавец: @{iduser_sellname} | Cумма: {i[6]} | Дата {i[3]} | Статус: {i[5]} \n''')
						doc.close()
					try:
						file = open(f'G{rand}.txt', encoding='utf8')
						bot.send_document(message.chat.id,file, caption='Cделки')
						file.close()
						os.remove(f'G{rand}.txt')
					except:
						bot.send_message(message.chat.id, 'Сдеелки отсудствуют', reply_markup=keyboards.admin)



			elif message.text.lower() == 'пользователи':
				if message.chat.id == config.admin:
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='Найти пользователя',callback_data='admin_search_user'))
					keyboard.add(types.InlineKeyboardButton(text='Найти пользователя id',callback_data='awfawfawfawfawfawfaw'))
					bot.send_message(message.chat.id, '<b>Нажми на кнопку</b>',parse_mode='HTML', reply_markup=keyboard)

			elif message.text.lower() == 'рассылка':
				if message.chat.id == config.admin:
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='С картинокй',callback_data=f'Рассылка{1}'))
					keyboard.add(types.InlineKeyboardButton(text='С гиф',callback_data=f'Рассылка{2}'))
					keyboard.add(types.InlineKeyboardButton(text='С видео',callback_data=f'Рассылка{3}'))
					bot.send_message(message.chat.id, f'''как будем рассылкать ?''',parse_mode='HTML', reply_markup=keyboard)


			elif message.text.lower() == '🤝 мои сделки':
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='✔️ Активные сделки',callback_data='my_sdelki'),types.InlineKeyboardButton(text='✖️ Закрытые сделки',callback_data='закрытыесделки'))
				bot.send_message(message.chat.id, "Какие сделки вас интересуют: ", reply_markup=keyboard)

			elif message.text.lower() == '🔍 найти пользователя':
				msg = bot.send_message(message.chat.id, f'<b>Введи username пользователя\n(Вводить нужно без @)</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg,searchuser)

			elif message.text.lower() == '🌐 информация':
				keyboard = types.InlineKeyboardMarkup()
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("SELECT url_ard FROM config  where id = "+str(1))
				url_ard = q.fetchone()[0]
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='🧑‍⚖️ Написать арбитру',url='{}'.format(arb_url)),types.InlineKeyboardButton(text='👨‍💻 Поддержка',url='{}'.format(help_url)))
				keyboard.add(types.InlineKeyboardButton(text='🗯 Чат пользователей ',url='{}'.format(chat_url)))
				bot.send_message(message.chat.id, f'''<b>Пользователи сервиса могут провести сделку 24/7, что, согласитесь, очень удобно.

Основные моменты:</b><i>
➖ Минимальная сумма сделки 10 RUB
➖ Оплата принимается в BTC BANKIR и QIWI. Выплата, соответственно, производится также
➖ Комиссия сервиса 8%
➖ Сумма сделки фиксируется в RUB в момент заключения сделки.</i>

<b>Открытие спора после оплаты Гарант-Сервиса.</b>
<i>➖ У покупателя и у продавца в процессе сделки есть кнопка "Открыть арбитраж". Сделка автоматически переходит в статус "Арбитраж". Продавец или покупатель должны написать Арбитру. После вынесения решения - денежные средства переводятся.</i>


<b>Внимание! Сделку должен начать Покупатель воспользовавшись поиском пользователей! Это важный момент.</b>''' ,parse_mode='HTML',disable_web_page_preview = True, reply_markup=keyboard)


			elif message.text.lower() == '🖥 кабинет':
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("SELECT balans FROM ugc_users where id is " + str(message.chat.id))
				balanss = q.fetchone()
				q.execute("SELECT raiting FROM ugc_users where id is " + str(message.chat.id))
				raiting = q.fetchone()
				q.execute("SELECT sdelka_colvo FROM ugc_users where id is " + str(message.chat.id))
				sdelka_colvo = q.fetchone()
				q.execute("SELECT sdelka_summa FROM ugc_users where id is " + str(message.chat.id))
				sdelka_summa = q.fetchone()
				balance = balanss[0]
				curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
				balanceusd = float(balance)*float(curse)


				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='⚜️ Пополнить баланс',callback_data=f'awhat_oplata'),types.InlineKeyboardButton(text='⚜️ Вывести',callback_data=f'awhat_wind'))
				keyboard.add(types.InlineKeyboardButton(text='👥 Партнерская программа',callback_data='fereralka'))
				keyboard.add(types.InlineKeyboardButton(text='🎁 Ваучеры',callback_data='vau'))

				bot.send_message(message.chat.id, f'''<b>🆔 Ваш id:</b> <code>{message.chat.id}</code>

<b>💰 Баланс:</b>

<b>➖ RUB:</b> <code>{balance}</code>

<b>♻️ Количество сделок:</b> <code>{sdelka_colvo[0]}</code>

<b>💳 Сумма сделок:</b> <code>{sdelka_summa[0]}</code> <b>RUB</b>

<b>📊 Рейтинг:</b> <code>{raiting[0]}</code>
		''',parse_mode='HTML', reply_markup=keyboard)

			elif message.text.lower() == 'назад':
				msg = bot.send_message(message.chat.id, '<b>Вернулись назад</b>',parse_mode='HTML', reply_markup=keyboards.main)

def new_admin(message):
	new_categ = message.text
	if new_categ != 'Отмена':
		try:
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			vr = '\n'+ str(message.text)
			q.execute(f"update config set id_arbtr = id || '{vr}'")
			connection.commit()		
			connection.close()
			bot.send_message(message.chat.id, 'Успешно!',parse_mode='HTML', reply_markup=keyboards.admin)
		except:
			bot.send_message(message.chat.id, 'Аргументы указаны неверно!',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',parse_mode='HTML', reply_markup=keyboards.admin)

def searchuser(message):
	if message.text.lower() != 'отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM ugc_users where upper(name) = '{message.text.upper()}'")
		row = q.fetchone()
		bot.send_message(message.chat.id, '<b>🔍 Ищем...</b>',parse_mode='HTML', reply_markup=keyboards.main)
		username = str(message.from_user.username)
		if row != None:
			if str(username) == str(row[1]):
				keyboard = types.InlineKeyboardMarkup()
				q.execute(f"SELECT name FROM ugc_users where id = '{row[0]}'")
				iduser_sellname = q.fetchone()[0]
				keyboard.add(types.InlineKeyboardButton(text='🔰 Открыть сделку',callback_data=f'Открытьсделку{row[0]}'))
				msg = bot.send_message(message.chat.id, f'''<b>Подробнее:</b>

<b>👤 Пользователь:</b> @{iduser_sellname}

<b>♻️ Количество сделок:</b> <code>{row[6]}</code>

<b>💳 Сумма сделок:</b> <code>{row[7]}</code> <b>RUB</b>

<b>📊 Рейтинг:</b> <code>{row[5]}</code>
	''',parse_mode='HTML')
			else:
				keyboard = types.InlineKeyboardMarkup()
				q.execute(f"SELECT name FROM ugc_users where id = '{row[0]}'")
				iduser_sellname = q.fetchone()[0]
				keyboard.add(types.InlineKeyboardButton(text='🔰 Открыть сделку',callback_data=f'Открытьсделку{row[0]}'))
				msg = bot.send_message(message.chat.id, f'''<b>Подробнее:</b>

<b>👤 Пользователь:</b> @{iduser_sellname}

<b>♻️ Количество сделок:</b> <code>{row[6]}</code>

<b>💳 Сумма сделок:</b> <code>{row[7]}</code> <b>RUB</b>

<b>📊 Рейтинг:</b> <code>{row[5]}</code>
	''',parse_mode='HTML', reply_markup=keyboard)

		else:
			bot.send_message(message.chat.id, '<b>Мы не нашли такого пользователя в базе!</b>',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '<b>Отменили</b>',parse_mode='HTML', reply_markup=keyboards.main)

def searchuserss(message):
	if message.text.lower() != 'отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM ugc_users where upper(name) = '{message.text.upper()}'")
		row = q.fetchone()
		bot.send_message(message.chat.id, '<b>🔍 Ищем...</b>',parse_mode='HTML', reply_markup=keyboards.main)
		username = str(message.from_user.username)
		if row != None:
			q.execute(f"SELECT name FROM ugc_users where id = '{row[0]}'")
			iduser_sellname = q.fetchone()[0]
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='➕ Изменить баланс',callback_data=f'добавитьбаланс_{row[0]}'))
			keyboard.add(types.InlineKeyboardButton(text='🔒 Заблокировать | Раблокировать',callback_data=f'заблокировать_{row[0]}'))
			bot.send_message(message.chat.id, f'''<b>Подробнее:</b>

<b>👤 Пользователь:</b> @{iduser_sellname}
<b>Баланс:</b> {row[2]}

<b>♻️ Количество сделок:</b> <code>{row[6]}</code>

<b>💳 Сумма сделок:</b> <code>{row[7]}</code>

<b>📊 Рейтинг:</b> <code>{row[5]}</code>

<b>Статус:</b> <code>{row[8]}</code>
''',parse_mode='HTML', reply_markup=keyboard)

		else:
			bot.send_message(message.chat.id, '<b>Мы не нашли такого пользователя в базе!</b>',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '<b>Отменили</b>',parse_mode='HTML', reply_markup=keyboards.main)

def searchuserss_1(message):
	if message.text.lower() != 'отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM ugc_users where id = '{message.text}'")
		row = q.fetchone()
		bot.send_message(message.chat.id, '<b>🔍 Ищем...</b>',parse_mode='HTML', reply_markup=keyboards.main)
		if row != None:
			q.execute(f"SELECT name FROM ugc_users where id = '{row[0]}'")
			iduser_sellname = q.fetchone()[0]
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='➕ Изменить баланс',callback_data=f'добавитьбаланс_{row[0]}'))
			keyboard.add(types.InlineKeyboardButton(text='🔒 Заблокировать | Раблокировать',callback_data=f'заблокировать_{row[0]}'))
			bot.send_message(message.chat.id, f'''<b>Подробнее:</b>

<b>👤 Пользователь:</b> @{iduser_sellname}
<b>Баланс:</b> {row[2]}

<b>♻️ Количество сделок:</b> <code>{row[6]}</code>

<b>💳 Сумма сделок:</b> <code>{row[7]}</code>

<b>📊 Рейтинг:</b> <code>{row[5]}</code>

<b>Статус:</b> <code>{row[8]}</code>
''',parse_mode='HTML', reply_markup=keyboard)

		else:
			bot.send_message(message.chat.id, '<b>Мы не нашли такого пользователя в базе!</b>',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '<b>Отменили</b>',parse_mode='HTML', reply_markup=keyboards.main)

def btc_oplata_1(message):
	if message.text != 'Отмена':
		if "https://telegram.me/BTC_CHANGE_BOT?" in str(message.text):
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("INSERT INTO btcbankir (user,text) VALUES ('%s', '%s')"%(message.chat.id,message.text))
			connection.commit()
			bot.send_message(message.chat.id, '♻️ Платеж проверяется, время зачисления 1-5 минут')
		else:
			bot.send_message(message.chat.id, f'⚒ Чек указан неверно!',parse_mode='HTML', reply_markup=keyboards.main)

	else:
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)

def comsaedit(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"update config set {str(comsa)} = '{message.text}' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def smena_id_uv(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"update config set {str(conf_uvs)} = '{message.text}' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)


def send_photoorno(message):
	if message.text != 'Отмена':
		global text_send_all
		text_send_all = message.text
		msg = bot.send_message(message.chat.id, 'Отправьте ссылку на медиа',parse_mode='HTML',disable_web_page_preview = True)
		bot.register_next_step_handler(msg, admin_send_message_all_text_rus)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)


def admin_send_message_all_text_rus(message):
	if message.text != 'Отмена':
		global media
		media = message.text
		if int(tipsend) == 1:
			msg = bot.send_photo(message.chat.id,str(media), "Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
				
		if int(tipsend) == 2:
			print(tipsend)
			msg = bot.send_animation(chat_id=message.chat.id, animation=media, caption="Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

		if int(tipsend) == 3:
			print(tipsend)
			media = f'<a href="{media}">.</a>'
			msg = bot.send_message(message.chat.id, f'''Отправить всем пользователям уведомление:
{text_send_all}
{media}
Если вы согласны, напишите Да''',parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def admin_send_message_all_text_da_rus(message):
	otvet = message.text
	colvo_send_message_users = 0
	colvo_dont_send_message_users = 0
	if message.text != 'Отмена':	
		if message.text.lower() == 'Да'.lower():
			connection = sqlite3.connect('database.sqlite')
			with connection:	
				q = connection.cursor()
				bot.send_message(message.chat.id, 'Начинаем отправлять!')
				if int(tipsend) == 1: # картинка
					q.execute("SELECT * FROM ugc_users")
					row = q.fetchall()
					for i in row:
						jobid = i[0]

						time.sleep(0.1)
						reply = json.dumps({'inline_keyboard': [[{'text': '✖️ Закрыть', 'callback_data': f'restart'}]]})
						response = requests.post(
							url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendPhoto"),
							data={'chat_id': jobid,'photo': str(media), 'caption': str(text_send_all),'reply_markup': str(reply),'parse_mode': 'HTML'}
						).json()
						if response['ok'] == False:
							colvo_dont_send_message_users = colvo_dont_send_message_users + 1
						else:
							colvo_send_message_users = colvo_send_message_users + 1;
					bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	

				elif int(tipsend) == 2: # гиф
					q.execute("SELECT * FROM ugc_users")
					row = q.fetchall()
					for i in row:
						jobid = i[0]

						time.sleep(0.1)
						reply = json.dumps({'inline_keyboard': [[{'text': '✖️ Закрыть', 'callback_data': f'restart'}]]})
						response = requests.post(
							url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendAnimation"),
							data={'chat_id': jobid,'animation': str(media), 'caption': str(text_send_all),'reply_markup': str(reply),'parse_mode': 'HTML'}
						).json()
						if response['ok'] == False:
							colvo_dont_send_message_users = colvo_dont_send_message_users + 1
						else:
							colvo_send_message_users = colvo_send_message_users + 1;
					bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	


				elif int(tipsend) == 3: # видео
					q.execute("SELECT * FROM ugc_users")
					row = q.fetchall()
					for i in row:
						jobid = i[0]
						time.sleep(0.2)
						response = requests.post(
							url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendMessage"),
							data={'chat_id': jobid, 'text': str(text_send_all) + str(media),'parse_mode': 'HTML'}
						).json()
						if response['ok'] == False:
							colvo_dont_send_message_users = colvo_dont_send_message_users + 1
						else:
							colvo_send_message_users = colvo_send_message_users + 1;
					bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)				



def add_money2(message):
   if message.text != 'Отмена':
      connection = sqlite3.connect('database.sqlite')
      q = connection.cursor()
      q.execute("update ugc_users set balans = balans +" + str( message.text ) +  " where id =" + str(id_user_edit_bal1))
      connection.commit()
      msg = bot.send_message(message.chat.id, 'Успешно!',parse_mode='HTML', reply_markup=keyboards.admin)
   else:
      bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)


def create_sdelka(message):
	global summa_sdelki
	summa_sdelki = message.text
	if summa_sdelki != 'Отмена':
		if message.content_type == 'text':
			try:
				if float(message.text) >= 10:
					msg = bot.send_message(message.chat.id, "<b>Введите условия сделки:</b>",parse_mode='HTML', reply_markup=keyboards.otmena)
					bot.register_next_step_handler(msg, create_sdelka1)
				else:
					bot.send_message(message.chat.id, '✖️ Не правильно указана сумма.',parse_mode='HTML',disable_web_page_preview = True, reply_markup=keyboards.main)
			except:
				bot.send_message(message.chat.id, 'Вернулись на главную',parse_mode='HTML', reply_markup=keyboards.main)
		else:
			bot.send_message(message.chat.id, '✖️ Вводить нужно число\nПовторите попытку', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',parse_mode='HTML', reply_markup=keyboards.main)


def create_sdelka1(message):
	opisaniesdelka = message.text
	if message.content_type == 'text':
		if opisaniesdelka != 'Отмена':
				#colvo = 1
				#dlina = 20
				#chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
				#for ttt in range(1):
				#	for n in range(20):
				#		id_sdelka =''
				#	for i in range(int(dlina)):
				#		id_sdelka += random.choice(chars)
				#print(id_sdelka)
				now = datetime.now()
				now_date = str(str(now)[:10])
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("INSERT INTO sdelki (user_create,user_invite,data,oplata,status,summa,info) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(message.chat.id,iduser_sell,now_date,'Нет','Открыта',summa_sdelki,opisaniesdelka))
				connection.commit()
				balance = summa_sdelki
				q.execute(f"SELECT name FROM ugc_users where id = '{iduser_sell}'")
				iduser_sellname = q.fetchone()[0]
				q.execute(f"SELECT name FROM ugc_users where id = '{message.chat.id}'")
				idubuyname = q.fetchone()[0]
				q.execute(f"SELECT seq FROM sqlite_sequence where name = 'sdelki'")
				id_sdelka = q.fetchone()[0]

				curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
				summarub = float(balance)*float(curse)

				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='Подтвердить',callback_data=f'подтвердить{id_sdelka}'))
				keyboard.add(types.InlineKeyboardButton(text='Отказаться',callback_data=f'отказсделка{id_sdelka}'))
				bot.send_message(message.chat.id, f'''🔰 Сделка: #G{id_sdelka} успешно создана.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Стоимость: <code>{summa_sdelki}</code> RUB

📝 Условия: <code>{opisaniesdelka}</code>

♻️ Статус: Ожидает подтверждения''',parse_mode='HTML', reply_markup=keyboards.main)

				bot.send_message(iduser_sell, f'''🔰 Сделка: #G{id_sdelka} успешно создана.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Стоимость: <code>{summa_sdelki}</code> RUB

📝 Условия: <code>{opisaniesdelka}</code>

♻️ Статус: Ожидает подтверждения''',parse_mode='HTML', reply_markup=keyboard)

		else:
			bot.send_message(message.chat.id, 'Вернулись на главную',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '✖️ Вводить нужно текст\nПовторите попытку', reply_markup=keyboards.main)





def vau_add(message):
	if message.content_type == 'text':
		if message.text.isdigit() == True and int(message.text) >= 1 and int(message.text) <= 99999999999999:
			if message.text != 'Отмена':
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				if message.text.isdigit() == True:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
					check_balans = q.fetchone()
					if float(check_balans[0]) >= int(message.text):
							colvo = 1
							dlina = 10
							chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
							for ttt in range(1):
								for n in range(10):
									id_sdelka =''
								for i in range(int(dlina)):
									id_sdelka += random.choice(chars)
							print(id_sdelka)
							q.execute("update ugc_users set balans = balans - "+str(message.text)+" where id = " + str(message.chat.id))
							connection.commit()
							q.execute("INSERT INTO vau (name,summa,adds) VALUES ('%s', '%s', '%s')"%(id_sdelka,message.text,message.chat.id))
							connection.commit()
							bot.send_message(message.chat.id, f'''🎁 Ваучер <code>{id_sdelka}</code>, успешно создан.''',reply_markup=keyboards.main, parse_mode='HTML')
							q.close()
							connection.close()
					else:
						msg = bot.send_message(message.chat.id, '⚠ Недостаточно средств')

				else:
					msg = bot.send_message(message.chat.id, '⚠ Ошибка!')
			else:
				bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)
		else:
			bot.send_message(message.chat.id, '✖️ Не правильно указана сумма.',parse_mode='HTML',disable_web_page_preview = True, reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '✖️ Вводить нужно число\nПовторите попытку', reply_markup=keyboards.main)
def new_token(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update config set qiwi_token = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def new_phone(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update config set qiwi_phone = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)
def card_viplata(message):
	qiwi_user = message.text
	if message.text != '🔶 Отменить':
		if qiwi_user[:1] == '4' and len(qiwi_user) == 16 or qiwi_user[:1] == '5' and len(qiwi_user) == 16:
			if qiwi_user.isdigit() == True:
				global numberphone
				numberphone = message.text
				msg = bot.send_message(message.chat.id, 'Введите сумму для выплаты')
				bot.register_next_step_handler(msg, summa_vilata_card)
			else:
				bot.send_message(message.chat.id, '📛 Неверно указан номер карты!',reply_markup=keyboards.main)
		else:
			msg = bot.send_message(message.chat.id, '📛 Неверно указан номер карты!')

	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def summa_vilata_card(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	if message.text.isdigit() == True:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT com_vivod FROM config  where id = "+str(1))
		com_vivod = q.fetchone()[0]
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(message.text):
				ref_prozent = com_vivod
				add_ref_money = int(message.text)/100*int(ref_prozent)
				sum_vivod = int(message.text) - int(add_ref_money)
				print(sum_vivod)
				q.execute("update ugc_users set balans = balans - "+str(message.text)+" where id = " + str(message.chat.id))
				connection.commit()
				q.execute("SELECT uv_vivod FROM config  where id = "+str(1))
				uv_vivod = q.fetchone()[0]
				bot.send_message(uv_vivod, f'#Вывод\n\nЗаказана выплата!\n\nПользовать: <a href="tg://user?id={message.chat.id}">{message.from_user.first_name}</a>\nИд: <code>'+str(message.chat.id)+'</code>\n\nCARD: <code>'+ str(numberphone)+'</code>\nСумма: <code>'+str(sum_vivod)+' </code>руб',parse_mode='HTML')
				bot.send_message(message.chat.id, f'''<b>✅ Выплата успешно заказана, ожидайте перевод !</b>

<b>ℹ️ Информация:</b>

<b>➖ Сумма выплаты:</b> <code>{sum_vivod}</code> <b>RUB (с учетом комиссий)</b>

<b>➖ Реквизиты:</b>  <code>{numberphone}</code>


''',reply_markup=keyboards.main, parse_mode='HTML')


				q.close()
				connection.close()
		else:
			msg = bot.send_message(message.chat.id, '⚠ Недостаточно средств')

	else:
		msg = bot.send_message(message.chat.id, '⚠ Ошибка!')

def btc_viplata(message):
	qiwi_user = message.text
	if message.text != '🔶 Отменить':
		global numberphone
		numberphone = message.text
		msg = bot.send_message(message.chat.id, 'Введите сумму для выплаты')
		bot.register_next_step_handler(msg, summa_vilata_btc)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def summa_vilata_btc(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	if message.text.isdigit() == True:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT com_vivod FROM config  where id = "+str(1))
		com_vivod = q.fetchone()[0]
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(message.text):
				ref_prozent = com_vivod
				add_ref_money = int(message.text)/100*int(ref_prozent)
				sum_vivod = int(message.text) - int(add_ref_money)
				print(sum_vivod)
				q.execute("update ugc_users set balans = balans - "+str(message.text)+" where id = " + str(message.chat.id))
				connection.commit()
				q.execute("SELECT uv_vivod FROM config  where id = "+str(1))
				uv_vivod = q.fetchone()[0]
				bot.send_message(uv_vivod, f'#Вывод\n\nЗаказана выплата!\n\nПользовать: <a href="tg://user?id={message.chat.id}">{message.from_user.first_name}</a>\nИд: <code>'+str(message.chat.id)+'</code>\nBTC: <code>'+ str(numberphone)+'</code>\nСумма: <code>'+str(sum_vivod)+' </code>руб',parse_mode='HTML')
				bot.send_message(message.chat.id, f'''<b>✅ Выплата успешно заказана, ожидайте перевод !</b>

<b>ℹ️ Информация:</b>

<b>➖ Сумма выплаты:</b> <code>{sum_vivod}</code> <b>RUB (с учетом комиссий)</b>

<b>➖ Реквизиты:</b>  <code>{numberphone}</code>


''',reply_markup=keyboards.main, parse_mode='HTML')


				q.close()
				connection.close()
		else:
			msg = bot.send_message(message.chat.id, '⚠ Недостаточно средств')

	else:
		msg = bot.send_message(message.chat.id, '⚠ Ошибка!')


def qiwi_viplata(message):
	qiwi_user = message.text
	if message.text != '🔶 Отменить':
		if qiwi_user[:1] == '7' and len(qiwi_user) == 11 or qiwi_user[:3] == '380' and len(qiwi_user[3:]) == 9 or qiwi_user[:3] == '375' and len(qiwi_user) <= 12:
			if qiwi_user.isdigit() == True:
				global numberphone
				numberphone = message.text
				msg = bot.send_message(message.chat.id, 'Введите сумму для выплаты')
				bot.register_next_step_handler(msg, summa_vilata_qiwi)
			else:
				bot.send_message(message.chat.id, '📛 Неверно указан кошелек!',reply_markup=keyboards.main)
		else:
			msg = bot.send_message(message.chat.id, '📛 Неверно указан кошелек!')

	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def summa_vilata_qiwi(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	if message.text.isdigit() == True:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT com_vivod FROM config  where id = "+str(1))
		com_vivod = q.fetchone()[0]

		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(message.text):
				ref_prozent = com_vivod
				add_ref_money = int(message.text)/100*int(ref_prozent)
				sum_vivod = int(message.text) - int(add_ref_money)
				print(sum_vivod)
				q.execute("update ugc_users set balans = balans - "+str(message.text)+" where id = " + str(message.chat.id))
				connection.commit()
				q.execute("SELECT uv_vivod FROM config  where id = "+str(1))
				uv_vivod = q.fetchone()[0]
				bot.send_message(uv_vivod, f'#Вывод\n\nЗаказана выплата!\n\nПользовать: <a href="tg://user?id={message.chat.id}">{message.from_user.first_name}</a>\nИд: <code>'+str(message.chat.id)+'</code>\n\nQiwi Кошелек: <code>'+ str(numberphone)+'</code>\nСумма: <code>'+str(sum_vivod)+' </code>руб',parse_mode='HTML')
				bot.send_message(message.chat.id, f'''<b>✅ Выплата успешно заказана, ожидайте перевод !</b>

<b>ℹ️ Информация:</b>

<b>➖ Сумма выплаты:</b> <code>{sum_vivod}</code> <b>RUB (с учетом комиссий)</b>

<b>➖ Реквизиты:</b>  <code>{numberphone}</code>


''',reply_markup=keyboards.main, parse_mode='HTML')


				q.close()
				connection.close()
		else:
			msg = bot.send_message(message.chat.id, '⚠ Недостаточно средств')

def vau_good(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM vau where name = '{message.text}'")
		status = q.fetchone()
		if status != None:
			print("yes")
			q.execute(f"SELECT summa FROM vau where name = '{message.text}'")
			summa = q.fetchone()
			q.execute(f"SELECT adds FROM vau where name = '{message.text}'")
			adds = q.fetchone()
			q.execute("update ugc_users set balans = balans + "+str(summa[0])+" where id = " + str(message.chat.id))
			connection.commit()
			print(summa[0])
			q.execute(f"DELETE FROM vau WHERE name = '{message.text}'")
			connection.commit()
			bot.send_message(message.chat.id, f'''🎁 Ваучер <code>{message.text}</code>, успешно активирован. Ваш баланс пополнен на <code>{summa[0]}</code> RUB. ''',reply_markup=keyboards.main, parse_mode='HTML')
			bot.send_message(adds[0], f'''👤  <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>  активировал(а) ваучер <code>{message.text}</code>.''',reply_markup=keyboards.main, parse_mode='HTML')

		else:
			bot.send_message(message.chat.id, f'''🎁 Ваучер <code>{message.text}</code>, не сушествует или уже активирован.''',reply_markup=keyboards.main, parse_mode='HTML')
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)
				
@bot.callback_query_handler(func=lambda call:True)
def podcategors(call):

	if call.data[:9] == 'my_sdelki':
		if call.data[9:] == '':
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='Как покупатель',callback_data='my_sdelki_buyer'))
			keyboard.add(types.InlineKeyboardButton(text='Как продавец',callback_data='my_sdelki_seller'))
			bot.send_message(call.message.chat.id, 'Выбери тип сделки', reply_markup=keyboard)

		elif call.data[9:] == '_seller':
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute(f"SELECT * FROM sdelki where user_invite = '{call.message.chat.id}'")
			info = q.fetchall()
			if info != None:
				keyboard = types.InlineKeyboardMarkup()
				for i in info:
					if str(i[5]) == str('Финал'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
					if str(i[5]) == str('Открыта'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
					if str(i[5]) == str('Оплачена'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
					if str(i[5]) == str('Ожидает оплаты'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
					if str(i[5]) == str('Арбитраж'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
				bot.send_message(call.message.chat.id, f'''Выберите сделку''', parse_mode='HTML', reply_markup=keyboard)
			else:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="У вас нет сделок такого типа")


		elif call.data[9:] == '_buyer':
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute(f"SELECT * FROM sdelki where user_create = '{call.message.chat.id}'")
			info = q.fetchall()
			if info != None:
				keyboard = types.InlineKeyboardMarkup()
				for i in info:
					if str(i[5]) == str('Финал'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
					if str(i[5]) == str('Открыта'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
					if str(i[5]) == str('Оплачена'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
					if str(i[5]) == str('Ожидает оплаты'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
					if str(i[5]) == str('Арбитраж'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
				bot.send_message(call.message.chat.id, f'''Выберите сделку''', parse_mode='HTML', reply_markup=keyboard)
			else:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="У вас нет сделок такого типа")


	if call.data[:12] == 'awhat_oplata':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup(row_width=2)
		keyboard.add(types.InlineKeyboardButton(text=f'🥝 QIWI',callback_data=f'Depoziit_qiwi'),types.InlineKeyboardButton(text=f'💵 BTC Чек',callback_data=f'бткчек'))
		bot.send_message(call.message.chat.id,  'Выбери способ для депозита', reply_markup=keyboard)

	if call.data[:13] == 'Depoziit_qiwi':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✅ Проверить',callback_data='Check_Depozit_qiwi_'))
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT qiwi_phone FROM config where id = '1'")
		qiwi_phone = q.fetchone()
		qiwi_oplata_url = "https://qiwi.com/payment/form/99?extra['account']="+str(qiwi_phone[0])+"&extra['comment']="+str(call.message.chat.id)+"&amountInteger=1&amountFraction=0&currency=643&blocked[1]=account&blocked[2]=comment"
		keyboard.add(types.InlineKeyboardButton(text='💳 Перейти к оплате',url=qiwi_oplata_url))
		bot.send_message(call.message.chat.id, f'''👉 Для пополнения баланса бота выполните рублёвый перевод по следующим реквизитам:

▫️ Кошелёк: <code>+{qiwi_phone[0]}</code>
▫️ Комментарий: <code>{call.message.chat.id}</code>

❗️ Не забудьте оставить комментарий к переводу

⏱ После перевода нажмите кнопку "ПРОВЕРИТЬ"''',parse_mode='HTML', reply_markup=keyboard)


	if call.data[:19] == 'Check_Depozit_qiwi_':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT qiwi_phone FROM config where id = 1")
		qiwi_phone = str(q.fetchone()[0])
		q.execute("SELECT qiwi_token FROM config where id = 1")
		qiwi_token = str(q.fetchone()[0])
		for payment in Qiwi(qiwi_token,qiwi_phone).get_payments(10, operation=OperationType.IN):
			q = q.execute('SELECT id FROM temp_pay WHERE txnid = ' + str(payment.raw['txnId']))
			temp_pay = q.fetchone()
			if 'RUB' in str(payment.currency) and str(payment.comment) == str(call.message.chat.id) and temp_pay == None and float(payment.amount) >= 1:
				q.execute("INSERT INTO temp_pay (txnid) VALUES ('%s')"%(payment.raw['txnId']))
				connection.commit()
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute(f"update ugc_users set balans = balans + '{payment.amount}' where id = '{call.message.chat.id}'")
				connection.commit()
				q.execute("SELECT uv_dep FROM config  where id = "+str(1))
				uv_dep = q.fetchone()[0]
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				bot.send_message(uv_dep, f'''Новый депозит на QIWI {payment.amount} RUB | <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> | <code>{call.message.chat.id}</code> ''',parse_mode='HTML')
				bot.send_message(call.message.chat.id, f"✅ На ваш баланс зачислено {payment.amount} RUB",parse_mode='HTML')
				q.execute(f"select ref from ugc_users where Id = '{call.message.chat.id}'")
				ref_user1 = q.fetchone()[0]
				if ref_user1 != '':
					add_deposit = int(payment.amount) / 100 * 2
					q.execute(f"update ugc_users set balans = balans + '{add_deposit}' where id = '{ref_user1}'")
					connection.commit()
					bot.send_message(ref_user1, f'Реферал пополнил баланс и вам зачислинно {add_deposit} RUB',parse_mode='HTML')
				break
			else:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Оплата не найдена!")

	if call.data == 'промоактивация':
		msg = bot.send_message(call.message.chat.id,f"<b>ℹ️ Отправьте промокод:</b>", reply_markup=keyboards.main, parse_mode='HTML')
		bot.register_next_step_handler(msg, aktivpromo)


	if call.data[:12] == 'бткчек':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id,'''👉 Для пополнения баланса BTC Чеком просто отправьте боту ЧЕК в личные сообщения.
Наша система автоматически проверит чек, время займет до 1 минуты

❗️ПРИНИМАЮТСЯ ТОЛЬКО РФ РУБЛИ

При возникновении ошибок пишите в тех. поддержку. Мы оперативно решим любую проблему.''', reply_markup=keyboards.main, parse_mode='HTML')
		bot.register_next_step_handler(msg, btc_oplata_1)



	elif call.data == 'create_sdelka':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.from_user.id,  '''ℹ️ Вы создаёте сделку как продавец.

💳 Введите сумму сделки:''', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, create_sdelka)

	elif call.data == 'invite_sdelka':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.from_user.id,  '🔰 Укажите id сделки', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, invite_sdelka)


	elif call.data[:11] == 'pay_sdelka_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT summa FROM sdelki where id = '{call.data[11:]}'")
		summa = q.fetchone()
		q.execute(f"SELECT user_create FROM sdelki where id = '{call.data[11:]}'")
		user_create = q.fetchone()
		q.execute("SELECT balans FROM ugc_users where id = "+ str(call.from_user.id))
		bal_us = q.fetchone()
		if int(bal_us[0]) >= int(summa[0]):
			q.execute("update ugc_users set balans = balans - " + str(summa[0])+" where id = " +str(call.from_user.id))
			connection.commit()
			q.execute(f"update sdelki set oplata = 'Да' where id = '{call.data[11:]}'")
			connection.commit()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='✔️ Товар получил ',callback_data=f'sdelka_good_{call.data[11:]}'))
			bot.send_message(call.from_user.id,  f'''📜 Сделка: #{call.data[11:]} оплачена.

ℹ️ Напишите: {user_create[0]} что бы получить товар !''', reply_markup=keyboard)
			bot.send_message(user_create[0], f'''📜 Сделка: #{call.data[11:]} оплачена.

ℹ️ Можете отправить товар покупателю: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> !''',parse_mode='HTML', reply_markup=keyboards.main)
		else:
			bot.send_message(call.from_user.id, 'Пополните баланс!', reply_markup=keyboards.main)


	elif call.data[:14] == 'otmena_sdelka_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		id_sdelka = call.data[14:]
		print(id_sdelka)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT user_create FROM sdelki where id = '{id_sdelka}'")
		user_create = q.fetchone()
		q.execute(f"SELECT user_invite FROM sdelki where id = '{id_sdelka}'")
		user_invite = q.fetchone()
		q.execute(f"update sdelki set status = 'Закрыта' where id = '{id_sdelka}'")
		connection.commit()
		q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
		uv_sdelki = q.fetchone()[0]
		bot.send_message(call.from_user.id,  f''''📜 Сделка: #{id_sdelka} отменена ! ''',parse_mode='HTML', reply_markup=keyboards.main)
		bot.send_message(user_create[0], f'''📜 Сделка: #{id_sdelka} отменена ! ''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data[:10] == 'otziv_yes_':
		global id_sdelka1
		id_sdelka1 = call.data[10:]
		print(id_sdelka1)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.from_user.id,  'ℹ️ Напишите текст отзыва:', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, otziv_yes)

	elif call.data[:9] == 'otziv_no_':
		id_sdelka = call.data[9:]
		print(id_sdelka)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT user_create FROM sdelki where id = '{id_sdelka}'")
		user_create = q.fetchone()
		q.execute(f"SELECT user_invite FROM sdelki where id = '{id_sdelka}'")
		user_invite = q.fetchone()
		if float(user_create[0]) == int(call.from_user.id):
			print('popal v user_create')
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='👍',callback_data=f'user_plus_{user_invite[0]}'),types.InlineKeyboardButton(text='👎',callback_data=f'user_minus_{user_invite[0]}'))
			bot.send_message(call.from_user.id,  'ℹ️ Оцените работу id юзера', reply_markup=keyboard)
		else:
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='👍',callback_data=f'user_plus_{user_create[0]}'),types.InlineKeyboardButton(text='👎',callback_data=f'user_minus_{user_create[0]}'))
			bot.send_message(call.from_user.id,  'ℹ️ Оцените работу id юзера', reply_markup=keyboard)

	elif call.data[:10] == "user_plus_":
		otziv_id = call.data[10:]
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT name FROM ugc_users where id = '{otziv_id}'")
		iduser_sellname = q.fetchone()[0]
		q.execute("update ugc_users set raiting = raiting + " + str('1')+" where id = " +str(otziv_id))
		connection.commit()
		bot.send_message(call.message.chat.id, f'''<b>❤️ Спасибо за оценку, рейтинг @{iduser_sellname} будет повышен !</b>''',parse_mode='HTML', reply_markup=keyboards.main)
		bot.send_message(otziv_id, f'''<b>👤 <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> повысил вам рейтинг !</b>''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data[:11] == "user_minus_":
		otziv_id = call.data[11:]
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT name FROM ugc_users where id = '{otziv_id}'")
		iduser_sellname = q.fetchone()[0]
		q = connection.cursor()
		q.execute("update ugc_users set raiting = raiting - " + str('2')+" where id = " +str(otziv_id))
		connection.commit()
		bot.send_message(call.message.chat.id, f'''<b>❤️ Спасибо за оценку, рейтинг @{iduser_sellname} будет понижен !</b>''',parse_mode='HTML', reply_markup=keyboards.main)
		bot.send_message(otziv_id, f'''<b>👤 <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> понизил вам рейтинг !</b>''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data == "awhat_wind":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='🥝 QIWI',callback_data=f'QIWI'),types.InlineKeyboardButton(text='💳 CARD',callback_data=f'CARD'))
		keyboard.add(types.InlineKeyboardButton(text='🥝 BTC',callback_data=f'BTC'),types.InlineKeyboardButton(text='💲 WMZ',callback_data=f'WMZ'))
		bot.send_message(call.message.chat.id, "<b>📤 Выберите платежную систему:</b>",parse_mode='HTML', reply_markup=keyboard)

	elif call.data == "QIWI":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "<b>📤 Введите ваш Qiwi Кошелек (Без +):</b>",parse_mode='HTML')
		bot.register_next_step_handler(msg, qiwi_viplata)

	elif call.data == "CARD":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "<b>📤 Введите ваш номер карты: (Visa или Mastercard)</b>",parse_mode='HTML')
		bot.register_next_step_handler(msg, card_viplata)

	elif call.data == "BTC":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "<b>📤 Введите ваш адрес BTC или ссылку на BTC BANKIR:</b>",parse_mode='HTML')
		bot.register_next_step_handler(msg, btc_viplata)

	elif call.data == "WMZ":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		bot.send_message(call.message.chat.id, "<b>Временно не доступно</b>",parse_mode='HTML')


	elif call.data == "vau":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='➕ Создать',callback_data=f'vau_add'),types.InlineKeyboardButton(text=' ✔️ Активировать',callback_data=f'vau_good'))
		bot.send_message(call.message.chat.id, "<b>Что вы бы хотели сделать?</b>",parse_mode='HTML', reply_markup=keyboard)

	elif call.data == "vau_add":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT balans FROM ugc_users where id is " + str(call.message.chat.id))
		balanss = q.fetchone()
		msg = bot.send_message(call.message.chat.id, f'''На какую сумму RUB выписать Ваучер ? (Его сможет обналичить любой пользователь, знающий код).

Доступно: {balanss[0]} RUB''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, vau_add)

	elif call.data == "vau_good":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '''Для активации ваучера отправьте его код:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, vau_good)


	elif call.data[:13]  == "Открытьсделку":
		global iduser_sell
		iduser_sell = call.data[13:]
		msg = bot.send_message(call.message.chat.id, "<b>Введите сумму сделки в RUB:</b>",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, create_sdelka)

	elif call.data[:11]  == "подтвердить":
		idsdelkas = call.data[11:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		try:
			status = q.execute(f'SELECT status FROM sdelki where id = "{idsdelkas}"').fetchone()[0]
			if str(status) == str('Открыта'):
				pokupatel = q.execute(f'SELECT user_create FROM sdelki where id = "{idsdelkas}"').fetchone()[0]
				summa = q.execute(f'SELECT summa FROM sdelki where id = "{idsdelkas}"').fetchone()[0]
				balance = summa
				curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
				summarub = float(balance)*float(curse)
				q.execute(f"update sdelki set status = 'Ожидает оплаты' where id = '{idsdelkas}'")
				connection.commit()
				q.execute(f"update sdelki set user_invite = '{call.message.chat.id}' where id = '{idsdelkas}'")
				connection.commit()
				q.execute(f"SELECT name FROM ugc_users where id = '{call.message.chat.id}'")
				iduser_sellname = q.fetchone()[0]
				q.execute(f"SELECT name FROM ugc_users where id = '{pokupatel}'")
				idubuyname = q.fetchone()[0]
				info = q.execute(f'SELECT info FROM sdelki where id = "{idsdelkas}"').fetchone()[0]

				bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{idsdelkas}

		➖ Покупатель: @{idubuyname}

		➖ Продавец: @{iduser_sellname}

		💰 Сумма: <code>{summa}</code> RUB

		📝 Условия: <code>{info}</code>

		♻️ Статус: Ожидайте уведомления об оплате''',parse_mode='HTML')
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='Оплатить',callback_data=f'оплатитьсделку{idsdelkas}'))
				keyboard.add(types.InlineKeyboardButton(text='Отменить',callback_data=f'отказсделка{idsdelkas}'))
				bot.send_message(pokupatel, f'''🔰 Сделка: #G{idsdelkas}

		➖ Покупатель: @{idubuyname}

		➖ Продавец: @{iduser_sellname}

		💰 Сумма: <code>{summa}</code> RUB

		📝 Условия: <code>{info}</code>

		♻️ Статус: Ожидание оплаты''',parse_mode='HTML', reply_markup=keyboard)
		except:
			print('ss')
		

	elif call.data[:14]  == "оплатитьсделку":
		idsdelkasa = call.data[14:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		try:
			status = q.execute(f'SELECT status FROM sdelki where id = "{idsdelkasa}"').fetchone()[0]
			if str(status) == str('Ожидает оплаты'):
				user_invite = q.execute(f'SELECT user_invite FROM sdelki where id = "{idsdelkasa}"').fetchone()[0]
				summa = q.execute(f'SELECT summa FROM sdelki where id = "{idsdelkasa}"').fetchone()[0]
				balance = summa
				curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
				summarub = float(balance)*float(curse)
				q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
				check_balans = q.fetchone()
				if float(check_balans[0]) >= float(summa):
					q.execute("update ugc_users set balans = balans - "+str(summa)+" where id = " + str(call.message.chat.id))
					connection.commit()
					q.execute(f"update sdelki set status = 'Оплачена' where id = '{idsdelkasa}'")
					connection.commit()
					q.execute(f"SELECT name FROM ugc_users where id = '{user_invite}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{call.message.chat.id}'")
					idubuyname = q.fetchone()[0]

					info = q.execute(f'SELECT info FROM sdelki where id = "{idsdelkasa}"').fetchone()[0]
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='Условия выполнены',callback_data=f'условиявыполнены{idsdelkasa}'))
					keyboard.add(types.InlineKeyboardButton(text='Возврат средств',callback_data=f'возвратсредств{idsdelkasa}'))
					q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
					uv_sdelki = q.fetchone()[0]
					bot.send_message(uv_sdelki, f'''🔰 Сделка: #G{idsdelkasa}

		ℹ️ Продавец: @{iduser_sellname} | Покупатель: @{idubuyname}

		💰 Сумма: <code>{summa}</code> RUB

		♻️ Статус: Новая сделка
		''',parse_mode='HTML')
					bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{idsdelkasa}

		➖ Покупатель: @{idubuyname}

		➖ Продавец: @{iduser_sellname}

		💰 Сумма: <code>{summa}</code> RUB

		📝 Условия: <code>{info}</code>

		♻️ Статус: Ожидайте передачу услуги/товара''',parse_mode='HTML', reply_markup=keyboards.main)

					bot.send_message(user_invite, f'''🔰 Сделка: #G{idsdelkasa}

		➖ Покупатель: @{idubuyname}

		➖ Продавец: @{iduser_sellname}

		💰 Сумма: <code>{summa}</code> RUB

		📝 Условия: <code>{info}</code>

		♻️ Статус: Оплачена, можете передавать товар/услугу''',parse_mode='HTML', reply_markup=keyboard)
				else:
					msg = bot.send_message(call.message.chat.id, '⚠ Недостаточно средств', reply_markup=keyboards.main)
		except:
			print('ss')
	elif call.data == 'fereralka':
		#bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT ref_colvo FROM ugc_users where id = " + str(call.from_user.id))
		ref_colvoo = q.fetchone()
		bot.send_message(call.from_user.id,  f'''<b>👥 Партнерская программа

▫️Что это?
Наша уникальная партнерская программа система позволит вам заработать крупную сумму без вложений. Вам необходимо лишь приглашать друзей и вы будете получать пожизненно 2% от их депозитов в боте.

📯 Ваша партнерская ссылка:</b>

https://t.me/getgarantbot?start={call.from_user.id}

<b>👥 Всего рефералов:</b> {ref_colvoo[0]}''', parse_mode='HTML',disable_web_page_preview = True, reply_markup=keyboards.main)
	elif call.data[:16]  == "условиявыполнены":
		saasasasss = call.data[16:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		status = q.execute(f'SELECT status FROM sdelki where id = "{saasasasss}"').fetchone()[0]
		if str(status) == str('Оплачена'):
			user_create = q.execute(f'SELECT user_create FROM sdelki where id = "{saasasasss}"').fetchone()[0]
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{saasasasss}"').fetchone()[0]
			balance = summa
			curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
			summarub = float(balance)*float(curse)
			q.execute(f"update sdelki set status = 'Финал' where id = '{saasasasss}'")
			connection.commit()
			info = q.execute(f'SELECT info FROM sdelki where id = "{saasasasss}"').fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{call.message.chat.id}'")
			iduser_sellname = q.fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{user_create}'")
			idubuyname = q.fetchone()[0]
			saassaddd = types.InlineKeyboardMarkup()
			saassaddd.add(types.InlineKeyboardButton(text='Открыть арбитраж',callback_data=f'арбитраж{saasasasss}'))
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='Отправить деньги продавцу',callback_data=f'отправитьбабкипродавцу{saasasasss}'))
			keyboard.add(types.InlineKeyboardButton(text='Открыть арбитраж',callback_data=f'арбитраж{saasasasss}'))
			bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{saasasasss}

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{summa}</code> RUB

📝 Условия: <code>{info}</code>

♻️ Статус: Закрыта, ожидайте подтверждения от покупателя
''',parse_mode='HTML', reply_markup=saassaddd)

			bot.send_message(user_create, f'''🔰 Сделка: #G{saasasasss}

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{summa}</code> RUB

📝 Условия: <code>{info}</code>

♻️ Статус: Условия выполнены''',parse_mode='HTML', reply_markup=keyboard)



	elif call.data[:22]  == "отправитьбабкипродавцу":
		idsdelkasaaassaa = call.data[22:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		status = q.execute(f'SELECT status FROM sdelki where id = "{idsdelkasaaassaa}"').fetchone()[0]
		if str(status) == str('Финал'):
			info = q.execute(f'SELECT info FROM sdelki where id = "{idsdelkasaaassaa}"').fetchone()[0]
			user_invite = q.execute(f'SELECT user_invite FROM sdelki where id = "{idsdelkasaaassaa}"').fetchone()[0]
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{idsdelkasaaassaa}"').fetchone()[0]
			balance = summa
			curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
			summarub = float(balance)*float(curse)
			q.execute("update ugc_users set balans = balans + "+str(summa)+" where id = " + str(user_invite))
			connection.commit()
			q.execute(f"update sdelki set status = 'Закрыта' where id = '{idsdelkasaaassaa}'")
			connection.commit()
			q.execute("update ugc_users set sdelka_summa = sdelka_summa + " + str(summa)+" where id = " +str(call.message.chat.id))
			connection.commit()
			q.execute("update ugc_users set sdelka_summa = sdelka_summa + " + str(summa)+" where id = " +str(user_invite))
			connection.commit()
			q.execute("update ugc_users set sdelka_colvo = sdelka_colvo + " + str('1')+" where id = " +str(call.message.chat.id))
			connection.commit()
			q.execute("update ugc_users set sdelka_colvo = sdelka_colvo + " + str('1')+" where id = " +str(user_invite))
			connection.commit()
			q.execute(f"SELECT name FROM ugc_users where id = '{user_invite}'")
			iduser_sellname = q.fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{call.message.chat.id}'")
			idubuyname = q.fetchone()[0]
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='👍',callback_data=f'user_plus_{call.message.chat.id}'),types.InlineKeyboardButton(text='👎',callback_data=f'user_minus_{call.message.chat.id}'))
			keyboardaa = types.InlineKeyboardMarkup()
			keyboardaa.add(types.InlineKeyboardButton(text='👍',callback_data=f'user_plus_{user_invite}'),types.InlineKeyboardButton(text='👎',callback_data=f'user_minus_{user_invite}'))
			q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
			uv_sdelki = q.fetchone()[0]
			bot.send_message(uv_sdelki, f'''🔰 Сделка: #G{idsdelkasaaassaa}

ℹ️ Продавец: @{iduser_sellname} | Покупатель: @{idubuyname}

💰 Сумма: <code>{summa}</code> RUB

♻️ Статус: Завершена успешно
''',parse_mode='HTML')
			bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{idsdelkasaaassaa}

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{summa}</code> RUB

📝 Условия: <code>{info}</code>

♻️ Статус: Завершена успешно''',parse_mode='HTML', reply_markup=keyboards.main)

			
			bot.send_message(user_invite, f'''🔰 Сделка: #G{idsdelkasaaassaa}

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{summa}</code> RUB

📝 Условия: <code>{info}</code>

♻️ Статус: Завершена успешно и вы получили {summa} RUB
''',parse_mode='HTML', reply_markup=keyboards.main)
			bot.send_message(call.message.chat.id, f'''ℹ️ Оцените работу @{iduser_sellname}''',parse_mode='HTML', reply_markup=keyboardaa)
			bot.send_message(user_invite, f'''ℹ️ Оцените работу @{idubuyname}''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:11]  == "отказсделка":
		idsdelkasaaaotkaz = call.data[11:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		user_create = q.execute(f'SELECT user_create FROM sdelki where id = "{idsdelkasaaaotkaz}"').fetchone()[0]
		user_invite = q.execute(f'SELECT user_invite FROM sdelki where id = "{idsdelkasaaaotkaz}"').fetchone()[0]
		q.execute(f"DELETE FROM sdelki WHERE id = '{idsdelkasaaaotkaz}'")
		connection.commit()
		q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
		uv_sdelki = q.fetchone()[0]
		bot.send_message(user_create, f'''🔰 Сделка: #G{idsdelkasaaaotkaz} Отменена''',parse_mode='HTML', reply_markup=keyboards.main)
		bot.send_message(user_invite, f'''🔰 Сделка: #G{idsdelkasaaaotkaz} Отменена''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data[:8]  == "арбитраж":
		arbitra = call.data[8:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		status = q.execute(f'SELECT status FROM sdelki where id = "{arbitra}"').fetchone()[0]
		if str(status) == str('Финал'):
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='Да',callback_data=f'арбитда{arbitra}'))
			bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{arbitra} вы подтверждаете открытия арбитража ?''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:7]  == "арбитда":
		arbitras = call.data[7:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		status = q.execute(f'SELECT status FROM sdelki where id = "{arbitras}"').fetchone()[0]
		if str(status) == str('Финал'):
			info = q.execute(f'SELECT info FROM sdelki where id = "{arbitras}"').fetchone()[0]
			user_invite = q.execute(f'SELECT user_invite FROM sdelki where id = "{arbitras}"').fetchone()[0]
			user_create = q.execute(f'SELECT user_create FROM sdelki where id = "{arbitras}"').fetchone()[0]
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{arbitras}"').fetchone()[0]
			balance = summa
			curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
			summarub = float(balance)*float(curse)
			q.execute(f"update sdelki set status = 'Арбитраж' where id = '{arbitras}'")
			connection.commit()
			q.execute(f"SELECT name FROM ugc_users where id = '{user_invite}'")
			iduser_sellname = q.fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{user_create}'")
			idubuyname = q.fetchone()[0]
			q.execute("SELECT uv_arb FROM config  where id = "+str(1))
			uv_arb = q.fetchone()[0]
			q.execute("SELECT url_ard FROM config  where id = "+str(1))
			url_ard = q.fetchone()[0]
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='Написать арбитру',url=url_ard))

			bot.send_message(uv_arb, f'''🔰 Сделка: #G{arbitras}

ℹ️ Продавец: @{iduser_sellname} | Покупатель: @{idubuyname}

💰 Сумма: <code>{summa}</code> RUB

♻️ Статус: Арбитраж
''',parse_mode='HTML')

			bot.send_message(user_create, f'''🔰 Сделка: #G{arbitras}

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{summa}</code> RUB

📝 Условия: <code>{info}</code>

♻️ Статус: Арбитраж
	''',parse_mode='HTML', reply_markup=keyboard)
			bot.send_message(user_invite, f'''🔰 Сделка: #G{arbitras}

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{summa}</code> RUB

📝 Условия: <code>{info}</code>

♻️ Статус: Арбитраж
	''',parse_mode='HTML', reply_markup=keyboard)






	elif call.data[:14]  == "возвратсредств":
		idsdelkasaaa = call.data[14:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		status = q.execute(f'SELECT status FROM sdelki where id = "{idsdelkasaaa}"').fetchone()[0]
		if str(status) == str('Оплачена'):
			user_create = q.execute(f'SELECT user_create FROM sdelki where id = "{idsdelkasaaa}"').fetchone()[0]
			info = q.execute(f'SELECT info FROM sdelki where id = "{idsdelkasaaa}"').fetchone()[0]
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{idsdelkasaaa}"').fetchone()[0]
			balance = summa
			curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
			summarub = float(balance)*float(curse)
			q.execute("update ugc_users set balans = balans + "+str(summa)+" where id = " + str(user_create))
			connection.commit()
			q.execute(f"update sdelki set status = 'Отменена' where id = '{idsdelkasaaa}'")
			connection.commit()
			q.execute(f"SELECT name FROM ugc_users where id = '{call.message.chat.id}'")
			iduser_sellname = q.fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{user_create}'")
			idubuyname = q.fetchone()[0]
			q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
			uv_sdelki = q.fetchone()[0]
			bot.send_message(uv_sdelki, f'''🔰 Сделка: #G{idsdelkasaaaotkaz} Отменена''',parse_mode='HTML')
			bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{idsdelkasaaa}

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{summa}</code> RUB

📝 Условия: <code>{info}</code>

♻️ Статус: Отменена''',parse_mode='HTML', reply_markup=keyboards.main)
			bot.send_message(user_create, f'''🔰 Сделка: #G{idsdelkasaaa}

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{summa}</code> RUB

📝 Условия: <code>{info}</code>

♻️ Статус: Отменена и средства вернулись на баланс''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data[:14]  == "просмотрсделки":
		prosmotridsdelka = call.data[14:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM sdelki where id = '{prosmotridsdelka}'")
		info = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		for i in info:
			if str(i[5]) == str('Арбитраж'):
				summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
				balance = i[6]
				curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
				summarub = float(balance)*float(curse)
				q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
				iduser_sellname = q.fetchone()[0]
				q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
				idubuyname = q.fetchone()[0]
				keyboard = types.InlineKeyboardMarkup()
				q.execute("SELECT url_ard FROM config  where id = "+str(1))
				url_ard = q.fetchone()[0]
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='Написать арбитру',url=url_ard))
				bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB  RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Арбитраж''',parse_mode='HTML', reply_markup=keyboard)

			if str(i[5]) == str('Финал'):
				if int(i[1]) == int(call.message.chat.id):
					#Покупатель
					summa = q.execute(f'SELECT summa FROM sdelki where id = "{prosmotridsdelka}"').fetchone()[0]
					balance = i[6]
					curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
					summarub = float(balance)*float(curse)
					q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
					idubuyname = q.fetchone()[0]
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='Отправить деньги продавцу',callback_data=f'отправитьбабкипродавцу{i[0]}'))
					keyboard.add(types.InlineKeyboardButton(text='Открыть арбитраж',callback_data=f'арбитраж{i[0]}'))
					bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Условия выполнены''',parse_mode='HTML', reply_markup=keyboard)
				else:
					#продавец
					q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
					idubuyname = q.fetchone()[0]
					summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
					balance = i[6]
					curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
					summarub = float(balance)*float(curse)
					saassaddd = types.InlineKeyboardMarkup()
					saassaddd.add(types.InlineKeyboardButton(text='Открыть арбитраж',callback_data=f'арбитраж{i[0]}'))
					bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Закрыта, ожидайте подтверждения от покупателя''',parse_mode='HTML', reply_markup=saassaddd)

			if str(i[5]) == str('Открыта'):
				if int(i[1]) == int(call.message.chat.id):
					q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
					idubuyname = q.fetchone()[0]
					balance = i[6]
					curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
					summarub = float(balance)*float(curse)
					bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Ожидаем подтверждения от продавца''',parse_mode='HTML', reply_markup=keyboards.main)
				else:
					q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
					idubuyname = q.fetchone()[0]
					balance = i[6]
					curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
					summarub = float(balance)*float(curse)
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='Подтвердить',callback_data=f'подтвердить{i[0]}'))
					keyboard.add(types.InlineKeyboardButton(text='Отказаться',callback_data=f'отказсделка{i[0]}'))
					summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
					bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]} успешно создана.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>
''',parse_mode='HTML', reply_markup=keyboard)

			if str(i[5]) == str('Оплачена'):
				if int(i[1]) == int(call.message.chat.id):
					q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
					idubuyname = q.fetchone()[0]
					balance = i[6]
					curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
					summarub = float(balance)*float(curse)
					summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
					bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Ожидайте передачу услуги/товара''',parse_mode='HTML', reply_markup=keyboards.main)
				else:
					q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
					idubuyname = q.fetchone()[0]
					balance = i[6]
					curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
					summarub = float(balance)*float(curse)
					summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='Условия выполнены',callback_data=f'условиявыполнены{i[0]}'))
					keyboard.add(types.InlineKeyboardButton(text='Возврат средств',callback_data=f'возвратсредств{i[0]}'))
					bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Оплачена, можете передавать товар/услугу''',parse_mode='HTML', reply_markup=keyboard)


			if str(i[5]) == str('Ожидает оплаты'):
				if int(i[1]) == int(call.message.chat.id):
					balance = i[6]
					q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
					idubuyname = q.fetchone()[0]
					curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
					summarub = float(balance)*float(curse)
					summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='Оплатить',callback_data=f'оплатитьсделку{i[0]}'))
					keyboard.add(types.InlineKeyboardButton(text='Отменить',callback_data=f'отказсделка{i[0]}'))
					bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Ожидание оплаты''',parse_mode='HTML', reply_markup=keyboard)
				else:
					q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
					idubuyname = q.fetchone()[0]
					balance = i[6]
					curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
					summarub = float(balance)*float(curse)
					summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
					bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Ожидайте уведомления об оплате''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data[:14]  == "закрытыесделки":
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='Как покупатель',callback_data=f'заксдел{1}'))
		keyboard.add(types.InlineKeyboardButton(text='Как продавец',callback_data=f'заксдел{2}'))
		bot.send_message(call.message.chat.id, 'Выбери тип сделки', reply_markup=keyboard)

	elif call.data[:11]  == "закарбитраж":
		idsdelkazak = call.data[11:]
		wdawdawdaw = idsdelkazak.split('\n')[2]
		colvoaktiv = idsdelkazak.split('\n')[1]
		sumpromo = idsdelkazak.split('\n')[0]
		print(colvoaktiv)
		print(sumpromo)
		print(wdawdawdaw)
		if int(wdawdawdaw) == 1:
			sssaa = 'в пользу покупателя'
		else:
			sssaa = 'в пользу продавца'
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"update sdelki set status = 'Закрыта' where id = '{colvoaktiv}'")
		connection.commit()
		q.execute(f"SELECT * FROM sdelki where id = '{colvoaktiv}'")
		info = q.fetchall()
		for i in info:
			q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
			iduser_sellname = q.fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
			idubuyname = q.fetchone()[0]
			balance = i[6]
			curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
			summarub = float(balance)*float(curse)
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
		q.execute("update ugc_users set balans = balans + "+str(i[6])+" where id = " + str(sumpromo))
		connection.commit()
		q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
		uv_sdelki = q.fetchone()[0]
		bot.send_message(uv_sdelki, f'''🔰 Сделка: #G{i[0]}

ℹ️ Продавец: @{iduser_sellname} | Покупатель: @{idubuyname}

💰 Сумма: <code>{summa}</code> RUB

♻️ Статус: Закрыта {sssaa}
''',parse_mode='HTML')

		bot.send_message(i[1], f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Закрыта {sssaa} ''',parse_mode='HTML', reply_markup=keyboards.main)
		bot.send_message(i[2], f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Закрыта {sssaa}''',parse_mode='HTML', reply_markup=keyboards.main)


	elif call.data[:8]  == "aaadddd_":
		idarbysd = call.data[8:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM sdelki where id = '{idarbysd}'")
		info = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		
		for i in info:
			q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
			iduser_sellname = q.fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
			idubuyname = q.fetchone()[0]
			balance = i[6]
			curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
			summarub = float(balance)*float(curse)
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
		keyboard.add(types.InlineKeyboardButton(text='Закрыть в пользу покупателя',callback_data=f'закарбитраж{i[1]}\n{idarbysd}\n{1}'))
		keyboard.add(types.InlineKeyboardButton(text='Закрыть в пользу продавца',callback_data=f'закарбитраж{i[2]}\n{idarbysd}\n{2}'))

		bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Арбитраж''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:14] == 'заблокировать_':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT status FROM ugc_users where id = "+ str(call.data[14:]))
		roww = q.fetchone()[0]
		if roww == 'Активен':
			q.execute(f"update ugc_users set status = 'Заблокирован' where id = {call.data[14:]}")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Заблокирован")
		else:
			q.execute(f"update ugc_users set status = 'Активен' where id = {call.data[14:]}")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Разблокирован")

	elif call.data[:16]  == "арбитрыудалить":
		msg = bot.send_message(message.chat.id, "Введите id админа", reply_markup = keyboards.otmena)
		bot.register_next_step_handler(msg,new_admin)

	elif call.data[:16]  == "изменитькоммисию":
		global comsa
		idedit = call.data[16:]
		if int(idedit) == 1:
			comsa = 'com_vvod'
		if int(idedit) == 2:
			comsa = 'com_vivod'
		if int(idedit) == 3:
			comsa = 'com_sdelka'
		msg = bot.send_message(call.message.chat.id, '''Отправьте новое значение:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, comsaedit)

	elif call.data[:20] == 'уведомлениянастройка':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT uv_dep FROM config  where id = "+str(1))
		uv_dep = q.fetchone()[0]
		q.execute("SELECT uv_arb FROM config  where id = "+str(1))
		uv_arb = q.fetchone()[0]
		q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
		uv_sdelki = q.fetchone()[0]
		q.execute("SELECT uv_vivod FROM config  where id = "+str(1))
		uv_vivod = q.fetchone()[0]
		q.execute("SELECT url_ard FROM config  where id = "+str(1))
		url_ard = q.fetchone()[0]
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='Изменить ид сделок',callback_data=f'edituv{1}'))
		keyboard.add(types.InlineKeyboardButton(text='Изменить ид арбитражей',callback_data=f'edituv{2}'))
		keyboard.add(types.InlineKeyboardButton(text='Изменить ид депозитов',callback_data=f'edituv{3}'))
		keyboard.add(types.InlineKeyboardButton(text='Изменить ид вывода',callback_data=f'edituv{4}'))
		keyboard.add(types.InlineKeyboardButton(text='Изменить ссылку арбитра',callback_data=f'edituv{5}'))
		bot.send_message(call.message.chat.id, f'''id для уведомления:

Сделка(Новая/Закрыта):{uv_sdelki}
Сделка(Арбитраж): {uv_arb}
Новые депозиты: {uv_dep}
Заявки на вывод: {uv_vivod}
Ссылка на арбитра: {url_ard}''',parse_mode='HTML', reply_markup=keyboard)
		
	elif call.data == 'изменитьтокен_':
		msg = bot.send_message(call.message.chat.id, 'Введи новый токен киви: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_token)

	elif call.data == 'изменитьномер_':
		msg = bot.send_message(call.message.chat.id, 'Введи новый номер: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_phone)

	elif call.data[:6] == 'edituv':
		global conf_uvs
		awfawfwa = call.data[6:]

		if int(awfawfwa) == 1:
			conf_uvs = 'uv_sdelki'
		if int(awfawfwa) == 2:
			conf_uvs = 'uv_arb'
		if int(awfawfwa) == 3:
			conf_uvs = 'uv_dep'
		if int(awfawfwa) == 4:
			conf_uvs = 'uv_vivod'
		if int(awfawfwa) == 5:
			conf_uvs = 'url_ard'

		msg = bot.send_message(call.message.chat.id, 'Введи новый id (Бот должен быть админом): ',parse_mode='HTML')
		bot.register_next_step_handler(msg, smena_id_uv)

	elif call.data[:15] == 'добавитьбаланс_':
		global id_user_edit_bal1
		id_user_edit_bal1 = call.data[15:]
		msg = bot.send_message(call.message.chat.id, 'Введи сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, add_money2)
			
	elif call.data[:17] == 'admin_search_user':
		msg = bot.send_message(call.message.chat.id, f'<b>Введи username пользователя\n(Вводить нужно без @)</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,searchuserss)

	elif call.data == 'awfawfawfawfawfawfaw':
		msg = bot.send_message(call.message.chat.id, f'<b>Введи id пользователя</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,searchuserss_1)

	elif call.data[:8] == 'Рассылка':
		global tipsend
		tipsend = call.data[8:]
		msg= bot.send_message(call.message.chat.id, "<b>Введи текст для рассылки</b>",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, send_photoorno)
			
	elif call.data[:7]  == "заксдел":
		ctosdelka = call.data[7:]
		if int(ctosdelka) == 1:
			status = 'user_create'
		else:
			status = 'user_invite'
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM sdelki where {str(status)} = '{call.message.chat.id}'")
		info = q.fetchall()
		rand = random.randint(10000000,99999999999)
		keyboard = types.InlineKeyboardMarkup()
		for i in info:
			if str(i[5]) == str('Закрыта'):
				q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
				iduser_sellname = q.fetchone()[0]
				q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
				idubuyname = q.fetchone()[0]
				doc = open(f'G{rand}.txt', 'a', encoding='utf8')
				doc.write(f'''ID: #G{i[0]} | Покупатель: @{idubuyname} | Продавец: @{iduser_sellname} | Cумма: {i[6]} | Дата {i[3]} | Статус: {i[5]} \n''')
				doc.close()
				
			if str(i[5]) == str('Отменена'):
				q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
				iduser_sellname = q.fetchone()[0]
				q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
				idubuyname = q.fetchone()[0]
				doc = open(f'G{rand}.txt', 'a', encoding='utf8')
				doc.write(f'''ID: #G{i[0]} | Покупатель: @{idubuyname} | Продавец: @{iduser_sellname} | Cумма: {i[6]} | Дата {i[3]} | Статус: {i[5]} \n''')
				doc.close()
		try:
			file = open(f'G{rand}.txt', encoding='utf8')
			bot.send_document(call.message.chat.id,file, caption='Ваши сделки')
			file.close()
			os.remove(f'G{rand}.txt')
		except:
			bot.send_message(call.message.chat.id, 'Сдеелки отсудствуют', reply_markup=keyboards.main)

		
















try:
	bot.polling(True)
except Exception as ex:
	bot.send_message(config.admin, f'Бот: @{config.bot_name} \n\nПоявилась ошибка: \n\n' +  str(ex))
