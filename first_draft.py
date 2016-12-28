#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup


# page_url = "http://www.immostreet.com/Listing/Search?sectionName=Rental&filter_place_id=55&set_localisation=Paris&place_id=4832012&search_type=6&property_type_id=1"
#
# path = "first_page.txt"
#
# page = ""
# if False:
#     page = requests.get(page_url).text
#     with open(path, 'w') as f:
#         f.write(page)
# else:
#     with open(path, 'r') as f:
#         page = f.read()
#
#
#
# soup = BeautifulSoup(page, 'html.parser')
# print(soup.find_all("div", { "class" : "item" }))



page_url = "http://www.seloger.com/immobilier/locations/immo-paris-75/bien-appartement/"
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
header = {'user-agent': ua}
r = requests.get(page_url, headers=header)
print(r.text)
