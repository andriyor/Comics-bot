#!/usr/bin/env python3

from random import (randint, choice)
from urllib import (request, error)

import telebot
from bs4 import BeautifulSoup
from requests import get
from config import token

bot = telebot.TeleBot(token)


def xkcd_link(n):
    try:
        page = 'http://xkcd.com/' + n + '/'
        response = request.urlopen(page)
        text = str(response.read())
        ls = text.find('embedding')
        le = text.find('<div id="transcript"')
        link = text[ls + 12:le - 2]
        print(link)
        return link
    except error.URLError:
        exit()


def xkcd_latest():
    try:
        new = request.urlopen('http://xkcd.com')
        content = str(new.read())
        ns = content.find('this comic:')
        ne = content.find('<br />\\nImage URL')
        newest = content[ns + 28:ne - 1]
        print(newest)
        return int(newest)
    except error.URLError:
        print('Network Error')
        print('Try again later')
        exit()
        return 0


def ru_xkcd_rand():
    response = get('http://xkcd.ru/num/')
    num_soup = BeautifulSoup(response.text, "html.parser")  # make soup that is parse-able by bs
    list_link = []
    for link in num_soup.find_all('a'):
        list_link.append(link.get('href'))
    link = choice(list_link[7:])
    return link


def ru_xkcd_link(n):
    img_link = ''
    page = 'http://xkcd.ru' + n
    response = get(page)
    s_img = BeautifulSoup(response.text, "html.parser")  # make soup that is parse-able by bs
    for img in s_img.find_all('img'):
        if img.parent.name == 'a':
            img_link = (img["src"])
            break
    print(img_link)
    return img_link


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_murkup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_murkup.row('/start', '/stop')
    user_murkup.row('q', 'xkcd')
    user_murkup.row('rxkcd', 'txkcd')
    bot.send_message(message.chat.id, 'Привет', reply_markup=user_murkup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "q":
        response = get('https://tproger.ru/wp-content/plugins/citation-widget/getQuotes.php')
        soup = BeautifulSoup(response.text, "html.parser")
        bot.send_message(message.chat.id, soup)

    elif message.text == "xkcd":
        val = str(randint(1, xkcd_latest()))
        if val == '404':
            bot.send_message(message.chat.id, 'Ты счастливчик')
        else:
            bot.send_message(message.chat.id, xkcd_link(val))

    elif message.text == "rxkcd":
        val = ru_xkcd_rand()
        if val == '/404/':
            bot.send_message(message.chat.id, 'Ты счастливчик')
        else:
            bot.send_message(message.chat.id, ru_xkcd_link(val))

    elif message.text == "txkcd":
        val = ru_xkcd_rand()
        if val == '/404/':
            bot.send_message(message.chat.id, 'Ты счастливчик')
        else:
            bot.send_message(message.chat.id, ru_xkcd_link(val))
            bot.send_message(message.chat.id, xkcd_link(val[1:-1]))
    else:
        bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True, interval=0)
