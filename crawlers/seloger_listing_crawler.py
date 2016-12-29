#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from stem import Signal
from stem.control import Controller
from stem import CircStatus


USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64)"
              + "AppleWebKit/537.36 (KHTML, like Gecko)"
              + "Chrome/55.0.2883.87"
              + "Safari/537.36")


def compose_url(min_price, page_nb):
    return ("http://www.seloger.com/list.htm"
            + "?idtt=1"  # renting=1, selling=2
            + "&cp=75"  # "code postal" of Paris
            + "&idtypebien=1"  # only appartements
            + "&pxmin=" + str(min_price)  # min price in €
            + "&tri=a_px"  # results sorted by price (in ascending order)
            + "&LISTING-LISTpg=" + str(page_nb))  # current page number


ads = {}
min_price, page_nb = 0, 1
n_results, cur_min_price = -1, -1

# After starting tor
tor  = "socks5://127.0.0.1:9150/"
proxyDict = { 
              "http" : tor, 
            }

count = 0
while True:
    # extraction of the soup of the page
    url = compose_url(min_price, page_nb)
    page = requests.get(url, headers={'user-agent': USER_AGENT}, proxies=proxyDict).text
    # with open("seloger.txt", 'r') as f:
    #     page = f.read()
    soup = BeautifulSoup(page, 'html.parser')

    # extraction of n_results
    if min_price == 0 and page_nb == 1:  # if first call
        assert n_results == -1  # n_results should be defined only the first time
        n_results_tags = soup.findAll("div", {"class": "title_nbresult"})
        assert len(n_results_tags) == 1  # there should be a single result count
        n_results_str = n_results_tags[0].contents[0]
        for c in [" ", " ", "annonces"]:  # /!\ the 2 invisible characters are different
            n_results_str = n_results_str.replace(c, "")
        n_results = int(n_results_str)
        print(n_results)

    # to know where we're at
    print(len(ads), "/", n_results)

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
    json_path = "seloger_listing_tmp.json"
    json_ads = {}
    if os.path.isfile(json_path):
        with open(json_path, 'rt') as f:
            json_ads = json.loads(f.read())
    json_ads.update(ads)
    json_dump = json.dumps(ads, indent=4)
    with open(json_path, 'w') as f:
        f.write(json_dump)

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
            break
        min_price = cur_min_price
        page_nb = 1
    assert page_nb < 101  # there are no more than 100 pages at a time in seloger.com

    if count % 500 == 0 :
    	# Asking for another IP address
        with Controller.from_port() as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)

            for circ in controller.get_circuits():
                if circ.status != CircStatus.BUILT:
                    continue

            exit_fp, exit_nickname = circ.path[-1]

            exit_desc = controller.get_network_status(exit_fp, None)
            exit_address = exit_desc.address if exit_desc else 'unknown'
            print ("  address: %s" % exit_address)

print(len(ads))


# import sys
# sys.exit(0)
# with open("seloger_tmp.txt", 'w') as f:
#     f.write(requests.get(compose_url(0, 100), headers={'user-agent': USER_AGENT}).text)
