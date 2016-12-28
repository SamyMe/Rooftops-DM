#!/usr/bin/env python3
import requests
from urllib.request import urlopen


page_url = "https://github.com/"
print(urlopen(page_url).read())
print(">" * 20 + " This was urllib ".ljust(40) + "<" * 20)
print(">" * 20 + " Press a key to continue ".ljust(40) + "<" * 20)

input()
print(requests.get(page_url).text)
print(">" * 20 + " This was requests ".ljust(40) + "<" * 20)


# ==== NOTES ====
# requests: http://docs.python-requests.org/en/master/
# urllib: https://docs.python.org/3/library/urllib.html
