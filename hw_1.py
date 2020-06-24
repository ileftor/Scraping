
# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного
# пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

user = 'ileftor'
#main_link = 'https://api.github.com/{user}/repos'
response = requests.get(f'https://api.github.com/users/{user}/repos')
data = response.json()
for i in response.json():
    if not i ['private']:
        print( i ['html_url'])
with open('gitrep.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)



# Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.


token = ''

response = requests.get(f'https://api.vk.com/method/groups.get?extended=1&access_token={token}&v=5.110. ')
data = response.json()
with open('vk_group.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)