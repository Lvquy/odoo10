# -*- coding: utf-8 -*-


import requests
def get_fbid(fb_url):
    URL = "https://findmyfbid.com/"
    PARAMS = {'url': fb_url}
    try:
        r = requests.post(url = URL, params= PARAMS)
        return r.json().get("id")
    except Exception:
        return 0
print get_fbid('otnon.ictu')