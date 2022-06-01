import sqlite3

qiwi_num = input('введи номер своего киви (без + )')
qiwi_token = input('введи токен своего киви')
admin_id = input('введи свой ID от телеграмм-аккаунта')
arb_id = input('введи ID арбитра')
help_id = input('введи ID поддержки')
com_sd = input('введи процент за сделки (только цифру)')
com_viv = input('введи процент за вывод (только цифру)')
com_vv = input('введи процент за ввод на балик (только цифру)')


connection = sqlite3.connect(database)
q = connection.cursor()

try:
    q.execute('UPDATE config SET qiwi_phone = "{}" WHERE id IS 1'.format(qiwi_num)
    except:
        print('чет пошло не так')
    connection.commit()
    connection.close()
    
try:
    q.execute('UPDATE config SET qiwi_phone = "{}" WHERE id IS 1'.format(qiwi_num)
    except:
        print('чет пошло не так')
    connection.commit()
    connection.close()
