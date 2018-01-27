# -*- coding: utf-8 -*-
import time
import re

import keyboard as keyboard
import telepot, requests
from telepot.loop import MessageLoop


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    r = requests.get(url)
    cash1 = r.json()
    lis1 = []
    for i in cash1:
        lis1.append(i["ccy"] + ' Buy: ' + i["buy"] + ' Sale: ' + i["sale"])
    p24 = "\n".join(lis1)
    print(p24)

    url2 = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
    k = requests.get(url2)
    cash2 = k.json()
    lis2 = []
    for i in cash2:
        if (i["cc"] == "RUB") or (i["cc"] == "USD") or (i["cc"] == "EUR"):
            lis2.append('1 ' + i["cc"] + ' = ' + str(i["rate"]) + '  ' + "UAH")
        nbu = "\n".join(lis2)
        print(nbu)

    if content_type != 'text':
        return

    if msg['text'] == '/p24':
        bot.sendMessage(chat_id, p24)
        return
    if msg['text'] == '/nbu':
        bot.sendMessage(chat_id, nbu)
        return

    if msg['text'] == '/rbi':
        bot.sendMessage(chat_id, "https://www.aval.ua/en/personal/everyday/exchange/exchange/converter/")
        return
    if msg['text'] == '/help':
        #keyboard()
        bot.sendMessage(chat_id, "/p24 - the currency rate of PrivatBank; \n /nbu - the currency rate of National Bank of Urkaine; \n/rbi - the link to page with currency exchange tool from Aval; \n "
                                 "To convert the currency use the template: \n 100usd=eur \n 100 eur = uah \n You will receive double converted course when convert without UAH (eur to usd or btc to eur)")

    if len(['' for i in msg['text'] if not i.isalpha()]) == len(msg['text']):
        bot.sendMessage(chat_id, eval(msg['text']))

    try:
        ppp = msg['text']
        pattern = re.compile(r'(\d+)\s*(\w+)\s*=\s*(\w+)')
        lp24=pattern.split(ppp)[1:-1]
        value = float(lp24[0])
        cur_from = lp24[1].upper()
        cur_to = lp24[-1].upper()
        url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
        r = requests.get(url)
        p24c = r.json()
        print('PrivatBank rate: ' + str(p24c))

        if cur_to == u'UAH':
            bot.sendMessage(chat_id, ('PrivatBank rate: ' + str("{0:.4f}".format((
                value * float([i['sale'] for i in p24c if i['ccy'] == cur_from][0])))) + ' ' + cur_to))
        if cur_from == u'UAH':
            bot.sendMessage(chat_id, (
            'PrivatBank rate: ' + str("{0:.4f}".format((value / float([i['buy'] for i in p24c if i['ccy'] == cur_to][0])))) + ' ' + cur_to))
        if "UAH" not in [cur_to, cur_from]:
            bot.sendMessage(chat_id, ('PrivatBank rate: ' + str("{0:.4f}".format((value * (float([i['buy'] for i in p24c if i['ccy'] == cur_from][0]))) / (float([i['sale'] for i in p24c if i['ccy'] == cur_to][0])))) + ' ' + cur_to))
    except Exception as e:
        print(e)

    try:
        m = msg['text']
        pattern = re.compile(r'(\d+)\s*(\w+)\s*=\s*(\w+)')
        lnbu=pattern.split(m)[1:-1]
        value1 = float(lnbu[0])
        cur_from = lnbu[1].upper()
        cur_to = lnbu[-1].upper()
        url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
        r = requests.get(url)
        nbuc = r.json()
        print('NBU rate: ' + str(nbuc))

        if cur_to == u'UAH':
            bot.sendMessage(chat_id, (
            'NBU rate: ' + str("{0:.4f}".format((value1 * float([i['rate'] for i in nbuc if i['cc'] == cur_from][0])))) + ' ' + cur_to))
        if cur_from == u'UAH':
            bot.sendMessage(chat_id, (
            'NBU rate: ' + str("{0:.4f}".format((value1 / float([i['rate'] for i in nbuc if i['cc'] == cur_to][0])))) + ' ' + cur_to))

        if "UAH" not in [cur_to, cur_from]:
            bot.sendMessage(chat_id, ('NBU rate: ' + str("{0:.4f}".format((value1 * (float([i['rate'] for i in nbuc if i['cc'] == cur_from][0])/ (float([i['rate'] for i in nbuc if i['cc'] == cur_to][0])))))) + ' ' + cur_to))
    except Exception as e:
        print(e)

TOKEN = '399090248:AAFuJVrVUbRY7gUZZYp6aEWLGqoO4vB7wuE'

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
