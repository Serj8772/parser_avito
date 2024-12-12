# import zipfile # включить при использовании proxy
# import re # включить при использовании proxy

import fake_useragent
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import fake_useragent
import telebot
import csv

from settings import token, id_channel, id_channel_for_logs, link, delay
# from settings import PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS

# настройка бота
bot = telebot.TeleBot(token)

# подменяем user-agent
user_agent = fake_useragent.UserAgent().random

opts = webdriver.ChromeOptions()
opts.add_argument(user_agent)
opts.add_argument("--disable-blink-features=AutomationControlled")
opts.add_argument('--headless') # запуск в фоновом режиме
opts.add_argument('--no-sandbox') # убирает ошибку запуска в headless режиме на сервере
# prefs = {"profile.managed_default_content_settings.javascript": 2} # отключаем javascript
# opts.add_experimental_option("prefs", prefs) # отключаем javascript

driver = webdriver.Chrome(options=opts)


while True:

    # загружаем ссылки из csv
    filename = 'links.csv'
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        existing_rows = list(reader)

    try:
        driver.implicitly_wait(20)          # ожидание появление элемента в секундах

        #  ссылка на страницу поиска
        driver.get(link) # заходим на сайт
        time.sleep(5)
        driver.save_screenshot(f'screenshots/screenshot'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'.png')
        bot.send_message(id_channel_for_logs, text=f'⚡️⚡️⚡️ СТАРТ АВИТО ⚡️⚡️⚡️\n{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

        # ищем объявления
        ssilki = driver.find_elements(By.CLASS_NAME, value='iva-item-title-CdRXl')

        for ssilka in ssilki:
            link = ssilka.find_element(By.TAG_NAME, 'a')


            # проверяем есть ли строка в файле, если нет то записываем ссылку
            def write_to_csv(filename, data):

                if [data] not in existing_rows:
                    with open(filename, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([data])
                    print(data, '--', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    bot.send_message(id_channel, text=data) # отправляем через бота в канал
                    time.sleep(5)

                else:
                    print('строка уже существует', '--', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


            data = link.get_attribute('href')
            write_to_csv(filename, data)


    except Exception as ex:
        print(ex)
        bot.send_message(id_channel_for_logs, text=f'⚡️⚡️⚡️ Ошибка ⚡️⚡️⚡️\n{ex}')

    time.sleep(delay * 60)