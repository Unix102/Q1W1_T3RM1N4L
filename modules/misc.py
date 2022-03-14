import os

from termcolor import colored

ban_account_desc = """Способ бана заключается в том, чтобы сделать как можно больше переводов на аккаунт жертвы
QIWI сочтет это за подозрительные переводы и забанит аккаунт.
Для лучшего эффекта можно переводить с комментариями "за соль", "за меф" и т.п

""" + colored("РАБОТОСПОСОБНОСТЬ НЕ ГАРАНТИРОВАНА!!", "red")

authors = colored("""Авторы данного скрипта:
@json1c (github: sergeyfilippov1, telegram: @json1c)
@batyarimskiy (github: batyarimskiy, telegram: @batyarimskiy)
@sorry69guys (telegram: @sorry69guys)""", "cyan")

banner = colored("""
░██████╗░██╗░██╗░░░░░░░██╗██╗
██╔═══██╗██║░██║░░██╗░░██║██║
██║██╗██║██║░╚██╗████╗██╔╝██║
╚██████╔╝██║░░████╔═████║░██║
░╚═██╔═╝░██║░░╚██╔╝░╚██╔╝░██║
░░░╚═╝░░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝""", "yellow")

def print_banner(count):
    os.system("cls")
    
    print(banner)
        
    print()
    print(f"Количество аккаунтов: {count}")
    print()

def menu(count):
    
    ch = input("> ")
    print_banner(count)
    
    return ch
