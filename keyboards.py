import telebot
from telebot import types

admin = telebot.types.ReplyKeyboardMarkup(True)
admin.row('Статистика','Рассылка')
admin.row('Настройки','Пользователи')
admin.row('Арбитражи','Cделки')



main = telebot.types.ReplyKeyboardMarkup(True)
main.row('🤝 Мои сделки','🖥 Кабинет')
main.row('🔍 Найти пользователя','🌐 Информация')

otmena = telebot.types.ReplyKeyboardMarkup(True)
otmena.row('Отмена')

otziv = telebot.types.ReplyKeyboardMarkup(True)
otziv.row('Да', 'Нет')
