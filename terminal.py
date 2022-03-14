
# ФАЙЛЫ ДЛЯ РАБОТЫ С БД: QiwiWrapper, DataBaseWrapper, accounts.db

# Комментариями помечены строки и куски взаимодействующие с БД.



from sqlite3.dbapi2 import connect
from SimpleQIWI import *
import os
import time
import sys
import random
import sqlite3
import requests
import json

from termcolor import colored
from SimpleQIWI.Errors import QIWIAPIError
from progress.bar import IncrementalBar

from modules import misc
from modules.qiwi_wrapper import QiwiWrapper
from modules.db_wrapper import DataBaseWrapper

db = DataBaseWrapper("accounts.db")
accounts = db.get_accounts()


misc.print_banner( len(accounts) )

proxy = input("Использовать прокси? (y/n) ")
print()

if proxy == "y":
    if os.path.exists("proxy.txt"):
        with open("proxy.txt", "r") as f:
            proxies = f.read()

            if not proxies:
                print("Заполните файл proxies.txt")
                sys.exit()
            else:
                proxies = proxies.split("\n")

    else:
        with open("proxy.txt", "x"):
            pass

        print("Заполните файл proxy.txt IP адресами прокси-серверов")
        print("Например:")
        print()
        print("http://1.3.45.66.22:8080")
        print("http://154.46.114:80")

        sys.exit()

else:
    proxies = ["http://localhost"]


misc.print_banner( len(accounts) )

if not accounts:
    token = input("Введите токен: ")
    login = input("Введите логин: ")
    session = requests.Session()
    session.headers['Accept']= 'application/json'
    session.headers['authorization'] = 'Bearer ' + token
    req = session.get("https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true").json()
    num = req['contractInfo']['contractId']

    qiwi_ = QiwiWrapper(token, login, proxy={"http": random.choice(proxies)})

    try:
        _ = qiwi_.api.balance               ######
        db.add_account(login, token)             #
                                                 #
        accounts = db.get_accounts()             #
        misc.print_banner( len(accounts) )       #
        print("Аккаунт добавлен!")          ######
        print("Помощь - /help")
        print('')

    except:
        print()
        print("Неверный токен!")
        sys.exit()

if len(accounts) == 1:
    qiwi = QiwiWrapper( accounts[0][1], accounts[0][0], proxy={"http": random.choice(proxies)} )
    token0 = {accounts[0][1]}
    num0 = {accounts[0][0]}
    token = ', '.join(token0)
    session = requests.Session()
    session.headers['Accept']= 'application/json'
    session.headers['authorization'] = 'Bearer ' + token
    req = session.get("https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true").json()
    num = req['contractInfo']['contractId']
    kiwi = QApi(token=token, phone=num)

################################################################
elif len(accounts) > 1:
    connect = sqlite3.connect('accounts.db')
    q = connect.cursor()
    res = q.execute("SELECT * FROM qiwi_accounts").fetchall()
    for i in res:                                                            
        print(f"{i[0]} | {i[1]}")                                                                       
                                                                                                                  
    print()                                                                                                       
                                                                                                                  
    while True:
        login = input("Выберите аккаунт: ") 
        try:                                                                      
            res = q.execute(f'SELECT * FROM qiwi_accounts where number = {login}').fetchone()
            qiwi = QiwiWrapper(res[1], res[0], proxy={"http": random.choice(proxies)})
            token0 = {res[1]}
            num0 = {res[0]}
            token = ', '.join(token0)
            session = requests.Session()
            session.headers['Accept']= 'application/json'
            session.headers['authorization'] = 'Bearer ' + token
            req = session.get("https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true").json()
            num = req['contractInfo']['contractId']
            misc.print_banner(len(accounts))
            kiwi = QApi(token=token, phone=num)
            break
        except Exception as e:
            print(e)
            print(f"Неверный токен!")
        
#########################################################################

kiwi = QApi(token=token, phone=num)
balance = kiwi.balance
print("+", num, sep='')
print("Баланс", str(balance[0]) + '₽')

while True:
        session = requests.Session()
        session.headers['Accept']= 'application/json'
        session.headers['authorization'] = 'Bearer ' + token
        req = session.get("https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true").json()
        token = ', '.join(token0)
        num = req['contractInfo']['contractId']
        kiwi = QApi(token=token, phone=num)
        
        print('')
        command = input('> ')

        if command == 'add':
            token = input("Введите токен: ")
            login = input("Введите логин: ")
            qiwi_ = QiwiWrapper(token, login, {"http": random.choice(proxies)})
            try:
                _ = qiwi_.api.balance
                db.add_account(login, token)
                accounts = db.get_accounts()
                misc.print_banner( len(accounts) )
                print("Аккаунт добавлен!")
            except:
                print()
                print("Неверный токен!")
            time.sleep(1)
            misc.print_banner( len(accounts) )
            balance = kiwi.balance
            print("+", num, sep='')
            print("Баланс", balance)                

        elif command == 'delete':
                number = input("Введите логин аккаунта для удаления: ")
                db.delete_account(number)
                accounts = db.get_accounts()
                misc.print_banner( len(accounts) )
                print("Аккаунт удалён!")
                time.sleep(1)
                misc.print_banner( len(accounts) )
                balance = kiwi.balance
                print("+", num, sep='')
                print("Баланс", balance)
        
        elif command == 'help':
            print('''
add - Добавить аккаунт
delete - Удалить аккаунт

pay - Перевести деньги
paylist - Список последних транзакций
ban - Забанить чужой аккаунт
update - Обновить баланс
profile - Узнать информацию об аккаунте
donate - Сгенерировать ссылку для получения платежей
authors - Список авторов''')
        
        elif command == 'update':
            kiwi = QApi(token=token, phone=num)
            os.system
            misc.print_banner( len(accounts) )
            balance = kiwi.balance
            print("+", num, sep='')
            print("Баланс", balance)

        elif command == 'pay':
            kiwi = QApi(token=token, phone=num)
            getter = input('Номер получателя без плюса: ')
            summ = input('Сумма перевода: ')
            while not summ.isdigit():
                print("Ты будешь переводить буквы?")
                summ = input('Сумма перевода: ')
            comment = input('Комментарий (Enter для пропуска): ')
            summa = float(summ)
            for item in balance:
                float(item)
            try:
                kiwi.pay(account=getter, amount=summa, comment=comment)
                print('Перевод совершен!')
                print('')
            except Exception as e:
                print('Недостаточно средств!')
                print('')
                print(e)
            time.sleep(1)
            misc.print_banner( len(accounts) )
            balance = kiwi.balance
            print("+", num, sep='')
            print("Баланс", balance)

        elif command == 'paylist':
            s = requests.Session()
            s.headers['authorization'] = 'Bearer ' + token  
            parameters = {'rows': 20}
            h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + str(num) + '/payments', params=parameters).json()
            x = 1
            for i in h['data']:
                sb = '-' if i['type'] == 'OUT' else '+'
                text = str(x) + '. ' + '[' + i['status'] + '] ' + sb + str(i['sum']['amount']) + '₽ ' + i['account'].replace('+', '') + ' (' + i['date'].split('T')[0] + ', ' + i['date'].split('T')[1].split('+')[0] + ')'
                if x < 10:
                    print(' ' + text)
                else:
                    print(text)
                x+=1

        elif command == 'donate':
            print('\nhttps://qiwi.com/payment/form/99?extra%5B%27account%27%5D=' + str(num) + '&amountInteger=1&amountFraction=0&extra%5B%27comment%27%5D=DONATE&currency=643&blocked[0]=account')

        elif command == 'ban':
            print()
            print(misc.ban_account_desc)
            print()
            number = input('Номер кошелька для бана: ')
            pays = input('Количество переводов (по 1 рублю): ')

            while not pays.isdigit():
                print("Количество нужно указывать цифрами!")
                pays = input('Количество переводов (по 1 рублю): ')

            comment = input('Комментарий к переводам (Enter для пропуска): ')
            print()

            if float(pays) > qiwi.api.balance[0]:
                print("Недостаточно средств!")

            else:
                bar = IncrementalBar( colored("Отправка платежей", "cyan"), max=int(pays))

                for _ in range( int(pays) ):
                    try:
                        qiwi.api.pay(
                            account=number,
                            amount=1,
                            comment=comment
                            )
                        time.sleep( 0.34 )
                        bar.next()
                    except:
                       print('Непредвиденная ошибка!')
                       break
            time.sleep(1)
            misc.print_banner( len(accounts) )
            balance = kiwi.balance
            print("+", num, sep='')
            print("Баланс", balance)

        elif command == 'profile':
            session = requests.Session()
            session.headers['Accept']= 'application/json'
            session.headers['authorization'] = 'Bearer ' + token
            try:
                req = session.get("https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true").json()
                req2 = session.get("https://edge.qiwi.com/identification/v1/persons/" + str(req['contractInfo']['contractId']) + "/identification").json()
                block = session.get('https://edge.qiwi.com/person-profile/v1/persons/' + str(req['contractInfo']['contractId']) + '/status/restrictions').json()
                
                blocked = req['contractInfo']['blocked']
                statusLvl = req['contractInfo']['identificationInfo'][0]['identificationLevel']
                phone = req['contractInfo']['contractId']
                nickname = req['contractInfo']["nickname"]["nickname"]
                date = req['contractInfo']['creationDate']
                ip = req["authInfo"]["ip"]
                email = req["authInfo"]["boundEmail"]

                print(statusLvl)

                if statusLvl == 'ANONYMOUS':
                    statusName = 'Минимальный'      
                elif statusLvl == 'SIMPLE' or statusLvl == 'VERIFIED':
                    statusName = 'Основной'    
                elif statusLvl == 'FULL':
                    statusName = 'Профессиональный'

                print()
                print("Информация об аккаунте:")
                print('Никнейм: ', nickname)
                print('Номер: +', phone, sep='')
                print('Статус: ', statusName)
                print('Дата регистрации:', date)
                print('Email:', email)
                print()

                if statusLvl == 'SIMPLE' or 'VERIFIED' or 'FULL':
                    print("Паспортные данные")
                    print("ФИО: " + req2["firstName"] + " " + req2["lastName"])
                    print("Дата рождения: " + req2["birthDate"])
                    print("Cерия и номер: " + req2["passport"])
                    print("ИНН: " + req2["inn"])
                    print()

                try:
                    if blocked != True:
                        print(block[0]['restrictionDescription'])
                    else:
                        print('Аккаунт полностью заблокирован')
                except:
                    print('Блокировки отсутствуют')
                print()

            except:
                print('Непредвиденная ошибка!')
                time.sleep(1)
                misc.print_banner( len(accounts) )
                balance = kiwi.balance
                print("+", num, sep='')
                print("Баланс", balance)

        elif command == 'authors':
            print()
            print(misc.authors)

        else:
            print('\nКоманды "' + command + '" не существует!')