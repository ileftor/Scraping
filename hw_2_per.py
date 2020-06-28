

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

vacancys = []

response = requests.get(link + p, headers=header)
while response.status_code == 200:
    response = response.text
    soup = bs(response, 'lxml')
    vacancy_block = soup.find('div', {'class': 'vacancy-serp'})
    vacancy_list = vacancy_block.find_all('div', {'class': 'vacancy-serp-item'})
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

        p = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        if p:
            p = p['href']
            response = requests.get(link + p, headers=header)
        else:
            break

print(len(vacancys))