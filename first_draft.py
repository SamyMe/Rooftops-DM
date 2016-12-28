#!/usr/bin/env python3
import requests


page_url = "http://www.immostreet.com/Listing/Search?sectionName=Rental&filter_place_id=55&set_localisation=Paris&place_id=4832012&search_type=6&property_type_id=1&price_min=&price_max=&area_min=&area_max=&nb_rooms_min=&nb_rooms_max="
print(requests.get(page_url).text)


# So I've made a comparison of different websites in info.txt
#   I think we should try immostreet.com, explorimmo.com and seloger.com in order
# The difficulty with seloger.com is that it uses Javascript a lot which make the crawling
#   more difficult
# I have compared urllib/requests/dryscrape/selenium in demos_requests/
#   There are a lot more alternatives but that's the only ones I have tested
#   urllib and requests are useless when the websites are using Javascript (like seloger.com)
#   dryscrape is better for that (cf 02_requests_vs_dryscrape.py)
#   selenium would also work but is super heavy
# So in the end I have decided to start with requests on immostreet.com and maybe we'll build
#   up on it later
# In demos_thenewboston/ there is a functional multithreaded crawler. It uses an architecture
#   that we don't need to follow at all, but it can give good ideas.
# Here it goes with immostreet.com, I'll parse it with beautifulsoup next time.
