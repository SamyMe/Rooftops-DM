#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import subprocess
import time
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from stem import Signal
from stem.control import Controller
from stem import CircStatus


PROXIES = {
    'http': 'socks5://localhost:9050',
    'https': 'socks5://localhost:9050'
}
USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
              + "Chrome/55.0.2883.87 Safari/537.36")
JSON_PATH = "seloger_listing_tmp.json"


def compose_url(min_price, page_nb):
    url = ("http://www.seloger.com/list.htm"
           + "?idtt=1"  # renting=1, selling=2
           + "&cp=75"  # "code postal" of Paris
           + "&idtypebien=1"  # only appartements
           + "&pxmin=" + str(min_price)  # min price in €
           + "&tri=a_px"  # results sorted by price (in ascending order)
           + "&LISTING-LISTpg=" + str(page_nb))  # current page number
    # print(url)  # for verbosity
    return url

def extract_n_ads(min_price):
    # extraction of the page's soup
    url = compose_url(min_price, 1)
    page = requests.get(url, headers={'user-agent': USER_AGENT}, proxies=PROXIES).text
    soup = BeautifulSoup(page, 'html.parser')

    # extraction of n_ads
    n_ads_tags = soup.findAll("div", {"class": "title_nbresult"})
    assert len(n_ads_tags) == 1  # there should be a single result count
    n_ads_str = n_ads_tags[0].contents[0]
    for c in [" ", " ", "annonce", "s"]:  # /!\ the 2 invisible characters are different
        n_ads_str = n_ads_str.replace(c, "")
    return int(n_ads_str)

def extract_max_price_from_json(path):
    if not os.path.isfile(path):
        return 0
    with open(path, 'rt') as f:
        json_ads = json.loads(f.read())
    prices = sorted([json_ads[ref]["price"] for ref in json_ads])
    return prices[-1]

def update_json(path, new_ads):
    json_ads = {}
    if os.path.isfile(JSON_PATH):
        with open(JSON_PATH, 'rt') as f:
            json_ads = json.loads(f.read())
    json_ads.update(new_ads)
    json_dump = json.dumps(json_ads, indent=4)
    with open(JSON_PATH, 'w') as f:
        f.write(json_dump)


subprocess.call(["systemctl", "restart", "tor"])  # just in case
time.sleep(5)  # wait for the end of the restart


ads = {}
min_price = extract_max_price_from_json(JSON_PATH)
page_nb = 1
local_n_ads = extract_n_ads(min_price)
total_n_ads = extract_n_ads(0)
cur_min_price = -1


count = 0
while True:
    # extraction of the soup of the page
    url = compose_url(min_price, page_nb)
    page = requests.get(url, headers={'user-agent': USER_AGENT}, proxies=PROXIES).text
    soup = BeautifulSoup(page, 'html.parser')

    # to know where we're at
    print("n_extracted:" + str(len(ads))
          + " | n_local:" + str(local_n_ads)
          + " | n_total:" + str(total_n_ads))

    # extraction of the ads and their info
    ad_tags = soup.find_all("article", {"class": ["listing", "life_annuity"]})  # list of ads
    assert len(ad_tags) < 21  # there should not be more than 20 ads per page
    for ad_tag in ad_tags:
        # extraction of the ids
        ad_dict = {}
        ad_id = ad_tag["data-listing-id"]  # the ad's id
        ad_dict["data-publication-id"] = ad_tag["data-publication-id"]  # the ad's id

        # extraction of the links and titles
        title_tags = ad_tag.select('h2 > a')  # selection of the title_tags
        assert len(title_tags) == 1  # there should be only one title_tag
        href = title_tags[0]["href"]
        ad_dict["href"] = href[0:href.find(".htm") + 4]  # link to the ad
        ad_dict["title"] = title_tags[0]["title"]  # text of the title

        # extraction of the prices
        price_tags = ad_tag.select('.amount')  # selection of the price_tags
        assert len(price_tags) == 1  # there should be only one price_tag
        price_str = price_tags[0].contents[0]
        assert "€" in price_str  # this should be a price
        for c in [" ", " ", "€", "\xa0"]:  # /!\ the 2 invisible characters are different
            price_str = price_str.replace(c, "")
        ad_dict["price"] = int(price_str)

        # fill ads dict and update cur_min_price
        ads[ad_id] = ad_dict
        cur_min_price = max(cur_min_price, ad_dict["price"])

    # update the json file incrementally
    update_json(JSON_PATH, ads)

    # prepare the move to next page
    next_buttons = soup.findAll("a", {"class": "pagination_next"})
    if len(next_buttons) == 2:  # there are 2 of them in the html for some reason
        next_url = next_buttons[0]["href"]
        page_nb_str = next_url[next_url.find("LISTING-LISTpg=") + 15:]
        page_nb += 1  # update page_nb so it can be crawled next iteration
        assert (page_nb) == int(page_nb_str)  # check that the next page_nb is correct
    else:
        assert(len(next_buttons) == 0)
        if page_nb < 100:
            with open("last_html_before_break.html", 'w') as f:
                f.write(page)
            break
        min_price = cur_min_price
        page_nb = 1
    assert page_nb < 101  # there are no more than 100 pages at a time in seloger.com

    if count % 20 == 0 and count != 0:
        subprocess.call(["systemctl", "restart", "tor"])
        time.sleep(1)  # wait for the end of the restart
        print("ID: ", requests.get("http://httpbin.org/ip", proxies=PROXIES).text)
        # with Controller.from_port() as controller:
        #     controller.authenticate()
        #     controller.signal(Signal.NEWNYM)
        #     for circ in controller.get_circuits():
        #         if circ.status != CircStatus.BUILT:
        #             continue
        #     exit_fingerprint, exit_nickname = circ.path[-1]
        #     exit_desc = controller.get_network_status(exit_fingerprint, None)
        #     exit_address = exit_desc.address if exit_desc else 'unknown'
        #     print ("  address: %s" % exit_address)
    count += 1


print("n_extracted:" + str(len(ads)))
