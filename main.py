#!/usr/bin/env python3
import os
from random import (randint, choice)
from urllib import (request, error)
from _datetime import datetime

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
    s_img = BeautifulSoup(response.text, 'html.parser')
    for img in s_img.find_all('img'):
        if img.parent.name == 'a':
            img_link = (img['src'])
            break
    print(img_link)
    return img_link


def get_dict_link_life():
    links = ['http://programmers.life']
    for i in range(2, 50):
        link = 'http://programmers.life/index-{}.html'.format(i)
        response = get(link)
        if response.status_code == 404:
            break
        else:
            links.append(link)
            print('page:', i, ' - ', link)

    print(links)

    img_links = []
    for link in links:
        response = get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_divs = soup.findAll('div', attrs={'class': 'entry'})
        print(link)
        for div in img_divs:
            img_link = div.find('img')['src']
            if 'tirinhaEN' in img_link:
                img_links.append(img_link)
                print('img: ', img_link)

    file = open('programmers_life.txt', 'w')
    for img_link in img_links:
        file.write("%s\n" % img_link)


def get_link_life():
    try:
        t = os.path.getmtime('programmers_life.txt')
        formats = '%Y-%m-%d'
        data = datetime.fromtimestamp(t).strftime(formats)
        if datetime.now().strftime(formats) != data:
            get_dict_link_life()
            return choice(list(open('programmers_life.txt')))
        else:
            return choice(list(open('programmers_life.txt')))
    except FileNotFoundError:
        get_dict_link_life()
        return choice(list(open('programmers_life.txt')))


def commitstrip_rlink():
    response = get('http://www.commitstrip.com/?random=1')
    soup = BeautifulSoup(response.text, "html.parser")
    url = soup.select_one('div.entry-content p img[src]')['src']
    return url


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_murkup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_murkup.row('/start', '/stop')
    user_murkup.row('q', 'xkcd', 'rxkcd',)
    user_murkup.row('txkcd', 'programmers.life', 'commitstrip')
    bot.send_message(message.chat.id, 'Привет', reply_markup=user_murkup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'q':
        response = get('https://tproger.ru/wp-content/plugins/citation-widget/getQuotes.php')
        soup = BeautifulSoup(response.text, 'html.parser')
        bot.send_message(message.chat.id, soup)

    elif message.text == 'xkcd':
        val = str(randint(1, xkcd_latest()))
        if val == '404':
            bot.send_message(message.chat.id, 'Ты счастливчик')
        else:
            bot.send_message(message.chat.id, xkcd_link(val))

    elif message.text == 'rxkcd':
        val = ru_xkcd_rand()
        if val == '/404/':
            bot.send_message(message.chat.id, 'Ты счастливчик')
        else:
            bot.send_message(message.chat.id, ru_xkcd_link(val))

    elif message.text == 'txkcd':
        val = ru_xkcd_rand()
        if val == '/404/':
            bot.send_message(message.chat.id, 'Ты счастливчик')
        else:
            bot.send_message(message.chat.id, ru_xkcd_link(val))
            bot.send_message(message.chat.id, xkcd_link(val[1:-1]))
    elif message.text == 'programmers.life':
        bot.send_message(message.chat.id, get_link_life())
    elif message.text == 'commitstrip':
        bot.send_message(message.chat.id, commitstrip_rlink())
    else:
        bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
