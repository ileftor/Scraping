
# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
# сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://mail.ru/')


elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172')

elem.send_keys(Keys.ENTER)

time.sleep(0.9)
elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NextPassword172')

elem.send_keys(Keys.ENTER)

# for i in range(10):
#     time.sleep(3)
#     classes = driver.find_elements_by_class_name('llc__container')
#     actions = ActionChains(driver)
#     actions.move_to_element(classes[-1])
#     actions.perform()




time.sleep(3)
mail = driver.find_element_by_class_name("llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal")
mail_link = mail.get_attribute('href')
driver.get(mail_link)



# for i in mail:
#     mail_link = mail.get_attribute('href')
#     print(mail_link)


#mail = driver.find_elements_by_class_name('llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal')

#print(mail)


#driver.quit()


# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары