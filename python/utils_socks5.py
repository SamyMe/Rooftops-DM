#!/usr/bin/env python3
import subprocess
import time
import requests


PROXIES = {'http': 'socks5://localhost:9050', 'https': 'socks5://localhost:9050'}
USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
              + "Chrome/55.0.2883.87 Safari/537.36")


def restart_tor(seconds_to_wait=1):
    subprocess.call(["systemctl", "restart", "tor"])
    time.sleep(seconds_to_wait)  # wait for the end of the restart


def requests_get(url, msg="", n_retries=10):
    for i in range(n_retries):
        try:
            page = requests.get(url, headers={'user-agent': USER_AGENT}, proxies=PROXIES).text
            assert "Une erreur s'est produite" not in page  # specific to seloger.com
            assert page is not None
            return page
        except:
            if msg != "":
                print("Request retry (" + msg + ")")
            if i < n_retries - 1:
                restart_tor(1)
    return None
