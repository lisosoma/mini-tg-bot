import re
import pandas as pd
import numpy as np
import telebot
import requests
import fake_useragent


def update():
    links, costs = [], []
    for i in range(5):
        user = fake_useragent.UserAgent().random
        headers = {
            "User-Agent": user}
        url = f"https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&foot_min=10&internet=1&maxprice=30000&mebel=1&minarea=30&offer_type=flat&only_foot=2&p={i}&region=1&rfgr=1&room1=1&sort=creation_date_desc&type=4&wm=1"
        r = requests.get(url=url, headers=headers)
        source_code = r.text
        links += re.findall(r'(https://www.cian.ru/rent/flat/[0-9]+/)+', source_code)
        costs += re.findall(r'[0-9 ]+ ₽/мес', source_code)
    links = np.array(links)
    costs = np.array(costs)
    df = pd.DataFrame(data=np.concatenate([links, costs]).reshape(2, len(links)).T, columns=['Ссылки', 'Цена'])
    return df
  
    
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Начал выполнение запроса")
        df = update()
        df.to_html('Объявления-Циан.html', render_links=True, escape=False)
        bot.send_message(message.from_user.id, f"""Последние 20 новых объявлений
{df.head(20)}""")
        bot.send_message(message.from_user.id, "Все объявления")
        bot.send_document(message.chat.id, open('Объявления-Циан.html', 'rb'))
  
  
bot = telebot.TeleBot('<YOUR BOT TOKEN>')
bot.polling(none_stop=True, interval=0)
