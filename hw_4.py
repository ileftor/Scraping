from pprint import pprint
from lxml import html
import requests
import re
from pymongo import MongoClient

# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# название источника,
# наименование новости,
# ссылку на новость,
# дата публикации




header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}



def request_to_lenta():
    major_link = 'https://lenta.ru/'
    response = requests.get(major_link, headers=header)
    dom = html.fromstring(response.text)

    newses_lenta = []
    news_block = dom.xpath("//div[@class='span8 js-main__content']/section[@class='row b-top7-for-main js-top-seven']/div[@class='span4']/div[@class='item'] | //div[@class='span8 js-main__content']/section[@class='row b-top7-for-main js-top-seven']/div[@class='span4']/div[@class='first-item']")
    for i in news_block:
        news = {}
        name = i.xpath(".//a/text()")
        link = i.xpath(".//time[@class='g-time']/../@href")
        date = i.xpath(".//a/time/@datetime")
        source = 'lenta.ru'

        news['source'] = source
        news['name'] = name
        news['link'] = link
        news['date'] = date
        newses_lenta.append(news)
    return (newses_lenta)


def request_to_yandex():
    major_link = 'https://yandex.ru/news/'
    response = requests.get(major_link, headers=header)
    dom = html.fromstring(response.text)
    newses_yandex = []
    news_block = dom.xpath("//div[@class='stories-set stories-set_main_no stories-set_pos_1']//td")

    for i in news_block:
        news = {}
        source = i.xpath(".//div[@class='story__date']/text()")
        name = i.xpath(".//h2/a/text()")
        link = i.xpath(".//h2/a/@href")
        date = i.xpath(".//div[@class='story__date']/text()")

        news['source'] = source
        news['name'] = name
        news['link'] = link
        news['date'] = date
        newses_yandex.append(news)
    return (newses_yandex)


listone = request_to_lenta()
listtwo = request_to_yandex()
all_news = []
all_news.extend(listone)
all_news.extend(listtwo)


# 2)Сложить все новости в БД

client = MongoClient('localhost', 27017)
db = client['news']
newsdb = db.news

for i in all_news:
    try:
        newsdb.insert_one(i)
    except:
        pass

for newsdb in newsdb.find({}):
    print(newsdb)