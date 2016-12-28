#!/usr/bin/env python3
import dryscrape
import requests


page_url = "http://www.seloger.com/immobilier/locations/immo-paris-75/bien-appartement/"
print(requests.get(page_url).text)
print(">" * 20 + " This was requests ".ljust(40) + "<" * 20)
print(">" * 20 + " Press a key to continue ".ljust(40) + "<" * 20)
input()

sess = dryscrape.Session()
sess.visit(page_url)
print(sess.body())
print(">" * 20 + " This was dryscrape ".ljust(40) + "<" * 20)
print(">" * 20 + " The difference comes from the header of the request ".ljust(40) + "<" * 20)


# ==== NOTES ====
# http://stackoverflow.com/a/26440563
# requests: http://docs.python-requests.org/en/master/
# dryscrape: https://dryscrape.readthedocs.io/en/latest/
