
# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
# сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172


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
driver.get('https://mail.ru/')


elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172')

elem.send_keys(Keys.ENTER)

time.sleep(0.9)
elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NextPassword172')

elem.send_keys(Keys.ENTER)

mails_link = []

for i in range(2):
    time.sleep(2)
    mail = driver.find_elements_by_xpath("//a[@class = 'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']")
    for i in mail:
        mail_link = i.get_attribute('href')
        if mail_link not in mails_link:
            mails_link.append(mail_link)
        else: continue
    classes = driver.find_elements_by_xpath("//a[@class = 'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']")
    actions = ActionChains(driver)
    actions.move_to_element(classes[-1])
    actions.perform()

mails = []

for i in mails_link:
    page = driver.get(i)
    time.sleep(3)
    mails_data = {}
    try:
        contact = driver.find_element_by_class_name('letter-contact')
        contact = contact.get_attribute('title')
    except:pass

    try:
        date = driver.find_element_by_class_name('letter__date').text
    except:
        pass

    try:
        topic = driver.find_element_by_class_name('thread__subject-line').text
    except:
        pass

    try:
        text = driver.find_element_by_class_name('letter__body').text
    except:
        pass

    mails_data['contact'] = contact
    mails_data['date'] = date
    mails_data['topic'] = topic
    mails_data['text'] = text
    mails.append(mails_data)

pprint(mails)
print(len(mails))

client = MongoClient('localhost', 27017)
db = client['mails']
mailsdb = db.mails

for i in mails:
    try:
        mailsdb.insert_one(i)
    except:
        pass

for mailsdb in mailsdb.find({}):
    print(mailsdb)



driver.quit()




