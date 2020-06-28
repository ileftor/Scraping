# 1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
# с сайта superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#
#   *Наименование вакансии
#   *Предлагаемую зарплату (отдельно мин. и отдельно макс. и отдельно валюта)
#   *Ссылку на саму вакансию
#   *Сайт откуда собрана вакансия


from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
import pandas as pd


#Для сайта hh


text = 'Data scientist'

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
link = 'https://hh.ru/'
p = f'search/vacancy?clusters=true&enable_snippets=true&text={text}&L_save_area=true&area=113&from=cluster_area&showClusters=true'

#Попыталась собрать все URL, но функция не работает
def search_page(link, p, header):
    pages = []
    response = requests.get(link + p, headers=header)
    while response.status_code == 200:
        response = response.text
        soup = bs(response, 'lxml')
        p = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        if p:
            p = p['href']
            pages.append(p)
            response = requests.get(link + p, headers=header)
        else:
            break
    return (pages)

pages = search_page(link, p, header)

print (pages)


#Для каждого URL ищем vacancy_list
# На этом этапе возникает ошибка, содержимое не всех страниц попадает в response
for i in pages:
    response = requests.get(link + i, headers=header).text
    soup = bs(response, 'lxml')
    vacancy_block = soup.find('div',{'class':'vacancy-serp'})
    vacancy_list = vacancy_block.find_all('div',{'class':'vacancy-serp-item'})

    vacancys = []
    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('a', {'class':'bloko-link HH-LinkModifier'}).getText()

        min_payment = vacancy.find('div', {'class':'vacancy-serp-item__sidebar'})
        if min_payment:
            min_payment = min_payment.getText()
            min_payment = min_payment.replace(u'\xa0', u' ')
            if re.fullmatch('.+-.+', min_payment):
                min_payment = re.findall('(\d+.\d+)-', min_payment)
                min_payment = [x.replace(' ', '') for x in min_payment]
                min_payment = int(min_payment[0])
            elif re.fullmatch('от.+', min_payment):
                min_payment = re.findall('(\d+.\d+)', min_payment)
                min_payment = [x.replace(' ', '') for x in min_payment]
                min_payment = int(min_payment[0])
            else:
                min_payment = None

        max_payment = vacancy.find('div', {'class':'vacancy-serp-item__sidebar'})
        if max_payment:
            max_payment = max_payment.getText()
            max_payment = max_payment.replace(u'\xa0', u' ')
            if re.fullmatch('.+-.+', max_payment):
                max_payment = re.findall('-(\d+.\d+)', max_payment)
                max_payment = [x.replace(' ', '') for x in max_payment]
                max_payment = int(max_payment[0])
            elif re.fullmatch('до.+', max_payment):
                max_payment = re.findall('(\d+.\d+)', max_payment)
                max_payment = [x.replace(' ', '') for x in max_payment]
                max_payment = int(max_payment[0])
            else:
                max_payment = None

        currency_payment = vacancy.find('div', {'class':'vacancy-serp-item__sidebar'})
        if currency_payment:
            currency_payment = currency_payment.getText()
            currency_payment = currency_payment.replace(u'\xa0', u' ')
            if re.fullmatch('.+', currency_payment):
                currency_payment = currency_payment.split()[-1]
            else:
                currency_payment = None

        vacancy_link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
        vacancy_source = 'hh'

        vacancy_data['name'] = vacancy_name
        vacancy_data['min_payment'] = min_payment
        vacancy_data['max_payment'] = max_payment
        vacancy_data['currency_payment'] = currency_payment
        vacancy_data['vacancy_link'] = vacancy_link
        vacancy_data['vacancy_source'] = vacancy_source
        vacancys.append(vacancy_data)


pprint(vacancys)
df_hh = pd.DataFrame(vacancys)
df_hh.head()