#!/usr/bin/env python3
import os
import requests
import time
import subprocess


PROXIES = { 'http': 'socks5://localhost:9050', 'https': 'socks5://localhost:9050' }
USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
              + "Chrome/55.0.2883.87 Safari/537.36")
PATH = os.path.dirname(os.path.abspath(__file__)) + "/local_page.html"
URL = "http://www.seloger.com/annonces/locations/appartement/paris-11eme-75/114842571.htm"


subprocess.call(["systemctl", "restart", "tor"])  # just in case
time.sleep(1)


page = requests.get(URL, headers={'user-agent': USER_AGENT}, proxies=PROXIES).text
with open(PATH, 'w') as f:
    f.write(page)
print(page)
