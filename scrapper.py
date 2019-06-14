# =============================================================================
# scrapper.py
# This module scraps a given URL for product information, i.e. name, price,
# description, and images.
# =============================================================================

from bs4 import BeautifulSoup as bs
import requests
import string
import time
import lxml
import urllib.request
import json

_AMAZON = 'https://amazon.com'
_WALMART = 'https://walmart.com'
url = 'https://www.amazon.com/PDX-Pet-Design-Licki-Brush/dp/B01M0UXYHE/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
r = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(r)
soup = bs(html, 'lxml')
title = soup.find("span", {"id": "productTitle"}).text.strip()

# Get price (as float)
# Scrapped as string in format "$##.##", then converted.
price = float(soup.find("span", {"id": "priceblock_ourprice"}).text[1:])

# Get description
# Scrapped bulleted-list as separate strings, then joined into one.
features = soup.find("div", {"id": "feature-bullets"})
ul_list = features.find("ul")
split_features = list(ul_list.stripped_strings)
desc = ' '.join(split_features)
print(desc)

# Parse HTML file for image links
data = json.loads(soup.find('script', type='').text)
urls = []
image_num = 0

