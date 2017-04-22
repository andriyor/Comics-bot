import os
from random import choice
from _datetime import datetime

import telebot
from bs4 import BeautifulSoup
import requests
from botanio import botan

botan_token = os.environ.get('BOTAN_API_KEY')

token = os.environ.get('TELEGRAM_API_KEY')
bot = telebot.TeleBot(token)


def xkcd_rand(link='http://c.xkcd.com/random/comic/'):
    try:
        response = requests.get(link, timeout=1)
        soup = BeautifulSoup(response.text, "html.parser")
        img_link = soup.select_one('div#comic img[src]')['src']
        return img_link
    except requests.exceptions.ConnectTimeout:
        return 'Oops. Connection timeout occurred!'


def ru_xkcd_rand():
    try:
        response = requests.get('http://xkcd.ru/num/', timeout=1)
        num_soup = BeautifulSoup(response.text, "html.parser")
        list_link = []
        real_li = num_soup.find_all("li", class_="real ")
        for li in real_li:
            list_link.append(li.find('a').get('href'))
        link = choice(list_link)
        return link
    except requests.exceptions.ConnectTimeout:
        return None


def ru_xkcd_link(n):
    page = 'http://xkcd.ru' + n
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_link = soup.select_one('div.main img[src]')['src']
    return img_link


def get_index_link_life():
    index_links = ['http://programmers.life']
    for i in range(2, 50):
        link = f'http://programmers.life/index-{i}.html'
        print(link)
        response = requests.get(link)
        if response.status_code == 404:
            break
        else:
            index_links.append(link)
    return index_links


def get_ing_link_life():
    img_links = []
    index_link = get_index_link_life()
    for link in index_link:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_divs = soup.findAll('div', attrs={'class': 'entry'})
        for div in img_divs:
            img_link = div.find('img')['src']
            if 'tirinhaEN' in img_link:
                img_links.append(img_link)
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
    try:
        response = requests.get('http://www.commitstrip.com/?random=1', timeout=1)
        soup = BeautifulSoup(response.text, "html.parser")
        link = soup.select_one('div.entry-content p img[src]')['src']
        return link
    except requests.exceptions.ConnectTimeout:
        return 'Oops. Connection timeout occurred!'


def explosm_rand():
    try:
        response = requests.get('http://explosm.net/comics/random', timeout=1)
        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.select_one('div.small-12.medium-12.large-12.columns img[src]')['src']
        return link
    except requests.exceptions.ConnectTimeout:
        return 'Oops. Connection timeout occurred!'


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_murkup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_murkup.row('/start', 'explosm')
    user_murkup.row('txkcd', 'xkcd', 'rxkcd',)
    user_murkup.row('tproger quote', 'commitstrip')
    bot.send_message(message.chat.id, 'Welcome to Comics Bot', reply_markup=user_murkup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'tproger quote':
        try:
            response = requests.get('https://tproger.ru/wp-content/plugins/citation-widget/getQuotes.php',
                                    timeout=1)
            soup = BeautifulSoup(response.text, 'html.parser')
            bot.send_message(message.chat.id, soup)
            botan.track(botan_token, uid=message.from_user.id, message='tproger quote', name='tproger quote')
        except requests.exceptions.ConnectTimeout:
            bot.send_message(message.chat.id, 'Oops. Connection timeout occurred!')
    elif message.text == 'xkcd':
        bot.send_message(message.chat.id, xkcd_rand())
        botan.track(botan_token, uid=message.from_user.id, message='xkcd', name='xkcd')
    elif message.text == 'explosm':
        bot.send_message(message.chat.id, explosm_rand())
        botan.track(botan_token, uid=message.from_user.id, message='explosm', name='explosm')
    elif message.text == 'rxkcd':
        val = ru_xkcd_rand()
        if val:
            bot.send_message(message.chat.id, ru_xkcd_link(val))
            botan.track(botan_token, uid=message.from_user.id, message='rxkcd', name='rxkcd')
        else:
            bot.send_message(message.chat.id, 'Oops. Connection timeout occurred!')
    elif message.text == 'txkcd':
        val = ru_xkcd_rand()
        if val:
            bot.send_message(message.chat.id, xkcd_rand(link=f'http://xkcd.com/{val}'))
            bot.send_message(message.chat.id, ru_xkcd_link(val))
            botan.track(botan_token, uid=message.from_user.id, message='txkcd', name='txkcd')
        else:
            bot.send_message(message.chat.id, 'Oops. Connection timeout occurred!')
    # elif message.text == 'programmers.life':
    #     bot.send_message(message.chat.id, get_link_life(message))
    elif message.text == 'commitstrip':
        bot.send_message(message.chat.id, commitstrip_rand())
        botan.track(botan_token, uid=message.from_user.id, message='commitstrip', name='commitstrip')
    else:
        bot.send_message(message.chat.id, 'Send me commands')

if __name__ == '__main__':
    bot.polling(none_stop=True)
