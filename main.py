#!/usr/bin/env python3
import os
from random import choice
from _datetime import datetime

import telebot
from bs4 import BeautifulSoup
from requests import get
from config import token

bot = telebot.TeleBot(token)


def xkcd_rlink(link='http://c.xkcd.com/random/comic/'):
    response = get(link)
    soup = BeautifulSoup(response.text, "html.parser")  # make soup that is parse-able by bs
    link = soup.select_one('div#comic img[src]')['src']
    return link


def ru_xkcd_rand():
    response = get('http://xkcd.ru/num/')
    num_soup = BeautifulSoup(response.text, "html.parser")  # make soup that is parse-able by bs
    list_link = []
    for link in num_soup.find_all('a'):
        list_link.append(link.get('href'))
    link = choice(list_link[7:])
    return link


def ru_xkcd_link(n):
    page = 'http://xkcd.ru' + n
    response = get(page)
    s_img = BeautifulSoup(response.text, 'html.parser')
    img_link = s_img.select_one('div.main img[src]')['src']
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


def get_link_life(mes):
    try:
        t = os.path.getmtime('programmers_life.txt')
        formats = '%Y-%m'
        data = datetime.fromtimestamp(t).strftime(formats)
        if datetime.now().strftime(formats) != data:
            get_dict_link_life()
            return choice(list(open('programmers_life.txt')))
        else:
            return choice(list(open('programmers_life.txt')))
    except FileNotFoundError:
        messages = 'This month you are the first who launched this command' \
                   'Wait about 30 seconds until the base is formed of links'
        bot.send_message(mes.chat.id, messages)
        get_dict_link_life()
        return choice(list(open('programmers_life.txt')))


def commitstrip_rlink():
    response = get('http://www.commitstrip.com/?random=1')
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.select_one('div.entry-content p img[src]')['src']
    return link


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
        bot.send_message(message.chat.id, xkcd_rlink())
    elif message.text == 'rxkcd':
        val = ru_xkcd_rand()
        bot.send_message(message.chat.id, ru_xkcd_link(val))
    elif message.text == 'txkcd':
        val = ru_xkcd_rand()
        bot.send_message(message.chat.id, xkcd_rlink(link='http://xkcd.com/{}'.format(val)))
        bot.send_message(message.chat.id, ru_xkcd_link(val))
    elif message.text == 'programmers.life':
        bot.send_message(message.chat.id, get_link_life(message))
    elif message.text == 'commitstrip':
        bot.send_message(message.chat.id, commitstrip_rlink())
    else:
        bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=True)
