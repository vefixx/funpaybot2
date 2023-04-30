from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle
from termcolor import colored
import os



url = r'https://funpay.com/account/login'
options = webdriver.ChromeOptions()
options.add_argument('headless=True')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=options)

print('Start')

filename = "settings.txt"

autoUp = None

# открытие файла на чтение и чтение текущего содержимого
with open(filename, "r") as f:
    lines = f.readlines()

# обработка строк содержимого файла
for line in lines:
    # поиск строки, содержащей нужную переменную
    if "AutoUp" in line:
        # разбиваем строку по символу "=" и берем вторую часть как значение переменной
        sett = line.split("=")[1].strip()
        print(sett)

# вывод значения переменной
autoUp = sett


print(colored(f'''Settings info:
Autoup: {autoUp}
''','magenta'))

driver.get(url)
time.sleep(1)
#load cookies for auto login
for cookie in pickle.load(open('FunPay_cookies', 'rb')):
    driver.add_cookie(cookie)
time.sleep(1)

#refresh browser
driver.refresh()
time.sleep(1)

driver.get('https://funpay.com/lots/1016/trade')
time.sleep(1)


while True:
    #переменные, которые изменяются
    f = open('data.txt', 'r').read() # открываем файл для чтения текущего баланса
    amount = int(f) #превращаем в целое число
    price_M = 4.4 #цена для покупателей
    price_for_me = 4 #цена для нас

    print(f"{colored('Get data from data.txt', 'green')} = {colored(amount, 'blue')}M")


    #found poduct on screen Million #####
    tovar_M = driver.find_element('xpath', '//*[@id="content"]/div/div/div[2]/div/div[2]/a').click()
    time.sleep(1)
    #Change product text on lot

    text = driver.find_element('xpath', '/html/body/div[2]/div/div/div[2]/form/div[2]/div/div[1]/input')
    text.clear()
    string = f"\u2604\uFE0F\u2604\uFE0FHypixel skyblock 1M - {str(price_M)}руб. В наличии {str(amount)}M! Безопасно и Быстро!\u2604\uFE0F\u2604\uFE0F"
    encoded = string.encode('utf-16')
    text.send_keys(encoded.decode('utf-16'))

    #change price current
    price = driver.find_element('xpath', '/html/body/div[2]/div/div/div[2]/form/div[3]/input')
    price.clear()
    price.send_keys(str(price_for_me))

    #change product amount in lot
    amount_values = driver.find_element('xpath', '/html/body/div[2]/div/div/div[2]/form/div[4]/input')
    amount_values.clear()
    amount_values.send_keys(str(amount))
    amount_values.send_keys(Keys.ENTER)
    time.sleep(1)

    #checked settings
    if autoUp == 'True':
        print(colored('Up lots', 'yellow'))
        button_up = driver.find_element('xpath', '//*[@id="content"]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/button').click()
    print(f'Price: {price_for_me}\nText: {string}\nValues: {amount}')
    print(colored(f'Status {colored("OK", "yellow")}', 'light_green'))
    
    time.sleep(30)
    os.system('cls')

driver.close()
driver.quit()