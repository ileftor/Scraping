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


#Для сайта hh


#https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=Data+scientist&L_save_area=true&area=113&from=cluster_area&showClusters=true

main_link = 'https://hh.ru/search/vacancy'
v = 'Data scientist'
v = v.split()
v_name = '+'.join(v)

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

params = {'clusters':True,
          'enable_snippets':True,
          'text':v_name,
          'L_save_area':True,
          'from':"cluster_area",
          'area':113,
          'showClusters':True
          }

response = requests.get(main_link,headers=header,params=params).text
pprint(response)

#soup = bs(response,'lxml')
#pprint(soup)

#vacancy_block = soup.find('div',{'class':'vacancy-serp'})
#pprint(vacancy_block)