#!/usr/bin/env python3
import os
from random import choice
from _datetime import datetime

import telebot
from bs4 import BeautifulSoup
from requests import get
from config import token

bot = telebot.TeleBot(token)


def xkcd_rand(link='http://c.xkcd.com/random/comic/'):
    response = get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    img_link = soup.select_one('div#comic img[src]')['src']
    return img_link


def ru_xkcd_rand():
    response = get('http://xkcd.ru/num/')
    num_soup = BeautifulSoup(response.text, "html.parser")
    list_link = []
    real_li = num_soup.find_all("li", class_="real ")
    for li in real_li:
        list_link.append(li.find('a').get('href'))
    return list_link


def ru_xkcd_link(n):
    page = 'http://xkcd.ru' + n
    response = get(page)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_link = soup.select_one('div.main img[src]')['src']
    return img_link


def get_index_link_life():
    index_links = ['http://programmers.life']
    for i in range(2, 50):
        link = 'http://programmers.life/index-{}.html'.format(i)
        response = get(link)
        if response.status_code == 404:
            break
        else:
            index_links.append(link)
            print('page:', i, ' - ', link)
    print(index_links)
    return index_links


def get_ing_link_life():
    img_links = []
    index_link = get_index_link_life()
    for link in index_link:
        response = get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_divs = soup.findAll('div', attrs={'class': 'entry'})
        print(link)
        for div in img_divs:
            img_link = div.find('img')['src']
            if 'tirinhaEN' in img_link:
                img_links.append(img_link)
                print('img: ', img_link)
    return img_links


def write_ing_link_life():
    with open('programmers_life.txt', 'w') as file:
        for img_link in get_ing_link_life():
            file.write("%s\n" % img_link)


def life_rand():
    with open('programmers_life.txt') as file:
        return choice(list(file))


def get_link_life(mes):
    try:
        t = os.path.getmtime('programmers_life.txt')
        formats = '%Y-%m'
        data = datetime.fromtimestamp(t).strftime(formats)
        if datetime.now().strftime(formats) != data:
            write_ing_link_life()
            return life_rand()
        else:
            return life_rand()
    except FileNotFoundError:
        messages = 'This month you are the first who launched this command' \
                   'Wait about 30 seconds until the base is formed of links'
        bot.send_message(mes.chat.id, messages)
        write_ing_link_life()
        return life_rand()


def commitstrip_rand():
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


# @bot.message_handler(content_types=['text'])
# def handle_text(message):
#     if message.text == 'q':
#         response = get('https://tproger.ru/wp-content/plugins/citation-widget/getQuotes.php')
#         soup = BeautifulSoup(response.text, 'html.parser')
#         bot.send_message(message.chat.id, soup)
#     elif message.text == 'xkcd':
#         bot.send_message(message.chat.id, xkcd_rand())
#     elif message.text == 'rxkcd':
#         val = ru_xkcd_rand()
#         bot.send_message(message.chat.id, ru_xkcd_link(val))
#     elif message.text == 'txkcd':
#         val = ru_xkcd_rand()
#         bot.send_message(message.chat.id, xkcd_rand(link='http://xkcd.com/{}'.format(val)))
#         bot.send_message(message.chat.id, ru_xkcd_link(val))
#     elif message.text == 'programmers.life':
#         bot.send_message(message.chat.id, get_link_life(message))
#     elif message.text == 'commitstrip':
#         bot.send_message(message.chat.id, commitstrip_rand())
#     else:
#         bot.send_message(message.chat.id, message.text)
#
# bot.polling(none_stop=True)

