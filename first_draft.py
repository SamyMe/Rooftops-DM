#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup


path = "seloger.txt"
page = ""
if not os.path.isfile(path):
    # print("Page comes from request")
    url = "http://www.seloger.com/list.htm?cp=75&idtt=1&idtypebien=1%2c2"
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    r = requests.get(url, headers={'user-agent': user_agent})
    page = r.text
    with open(path, 'w') as f:
        f.write(page)
else:
    # print("Page comes from local file")
    with open(path, 'r') as f:
        page = f.read()


soup = BeautifulSoup(page, 'html.parser')

data = soup.find_all("article")  # first we extract all the articles in the list

a_tags = data[0].select('h2 > a')  # selection of the title's tag
assert len(a_tags) == 1
title = a_tags[0]["title"]
href = a_tags[0]["href"]
print(title)
print(href)
