
# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')




block = driver.find_elements_by_class_name("accessories-product-list")
block = block[2]
goods = block.find_elements_by_class_name('gallery-list-item')

goods_list = []

i = 0
while i < 4:
    for good in goods:
        info = good.find_element_by_tag_name('a')
        info = info.get_attribute('data-product-info')
        goods_list.append(info)

        g = block.find_elements_by_tag_name('li')
        actions = ActionChains(driver)
        actions.move_to_element(g[3])
        actions.perform()


    button = driver.find_elements_by_class_name("accessories-carousel-wrapper")
    button = button[2]
    button = button.find_elements_by_tag_name('a')
    button = button[-1]
    button.click()

    i += 1

#pprint(goods_list)

driver.quit()



client = MongoClient('localhost', 27017)
db = client['hits']
hitsdb = db.hits

for i in goods_list:
        hitsdb.insert_one(i)

for hitsdb in hitsdb.find({}):
    print(hitsdb)




