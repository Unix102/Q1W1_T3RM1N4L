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





def add():
    token = input("Введите токен: ")
    number = input("Введите логин: ")
    qiwi_ = QiwiWrapper(token, number, {"http": random.choice(proxies)})
    try:
        _ = qiwi_.api.balance
        db.add_account(number, token)
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
    



def delete():
    number = input("Введите номер для удаления: ")
    db.delete_account(number)
    accounts = db.get_accounts()
    misc.print_banner( len(accounts) )
    print("Аккаунт удалён!")
    time.sleep(1)
    misc.print_banner( len(accounts) )
    balance = kiwi.balance
    print("+", num, sep='')
    print("Баланс", balance)




def help():
    print('''\n/update - Обновить баланс
/add - Добавить аккаунт
/delete - Удалить аккаунт
/send - Перевести деньги
/ban - Забанить чужой аккаунт
/profile - Узнать информацию об аккаунте
/authors - Список авторов''')




def update():
    kiwi = QApi(token=token, phone=num)
    os.system
    misc.print_banner( len(accounts) )
    balance = kiwi.balance
    print("+", num, sep='')
    print("Баланс", balance)




def send():
    kiwi = QApi(token=token, phone=num)
    getter = input('Номер получателя без плюса: ')
    summ = input('Сумма перевода: ')
    while not summ.isdigit():
        print("Ты будешь переводить буквы?")
        summ = input('Сумма перевода: ')
    comment = input('Комментарий (Enter для пропуска): ')
    summa = float(summ)
    procent = summa / 100 * 8.8 + summa
    for item in balance:
        float(item)
    if procent > item:
        print('Недостаточно средств!')
        print('')
    if procent <= item:
        try:
            kiwi.pay(account=getter, amount=summa, comment=comment)
            print('Перевод совершен!')
            print('')
        except:
            print('Непредвиденная ошибка!')
    time.sleep(1)
    misc.print_banner( len(accounts) )
    balance = kiwi.balance
    print("+", num, sep='')
    print("Баланс", balance)




def ban():
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
            qiwi.api.pay(
                account=number,
                amount=1,
                comment=comment
                )
            time.sleep( 0.34 )
            bar.next()
                    
    time.sleep(1)
    misc.print_banner( len(accounts) )
    balance = kiwi.balance
    print("+", num, sep='')
    print("Баланс", balance)




def profile():
    session = requests.Session()
    session.headers['Accept']= 'application/json'
    session.headers['authorization'] = 'Bearer ' + token
    req = session.get("https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true").json()
    req2 = session.get("https://edge.qiwi.com/identification/v1/persons/" + str(req['contractInfo']['contractId']) + "/identification").json()
            
    statusLvl = req['contractInfo']['identificationInfo'][0]['identificationLevel']
    phone = req['contractInfo']['contractId']
    nickname = req['contractInfo']["nickname"]["nickname"]
    date = req['contractInfo']['creationDate']
    ip = req["authInfo"]["ip"]
    email = req["authInfo"]["boundEmail"]

    if statusLvl == 'ANONYMOUS':
        statusName = 'Минимальный'      
    if statusLvl == 'SIMPLE':
        statusName = 'Основной'
    if statusLvl == 'VERIFIED':
        statusName = 'Основной'    
    if statusLvl == 'FULL':
        statusName = 'Профессиональный'

    print('')
    print("Информация об аккаунте:")
    print('Никнейм: ', nickname)
    print('Номер: +', phone, sep='')
    print('Статус: ', statusName)
    print('Дата регистрации:', date)
    print('Email:', email)
    print('')
    if statusLvl == 'SIMPLE' or 'VERIFIED' or 'FULL':
        print("Паспортные данные")
        print("ФИО: " + req2["firstName"] + " " + req2["lastName"])
        print("Дата рождения: " + req2["birthDate"])
        print("Cерия и номер: " + req2["passport"])
        print("ИНН: " + req2["inn"])
        print('')




def authors():
    print()
    print(misc.authors)
