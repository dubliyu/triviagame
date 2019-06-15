# =============================================================================
# scraper.py
# This module scraps a given URL for product information, i.e. name, price,
# description, and images.
# =============================================================================
#
# NOTE: Only tested with Amazon so far.
# NOTE 2: Will probably define a Scraper class, which will be passed a URL
#

from bs4 import BeautifulSoup as bs
import string
import lxml
import urllib.request
import json
import re

# Removes HTML tags from a string.
def remove_tags(string):
  tag = re.compile(r'<[^>]+>')
  return tag.sub('', string)

_AMAZON = 'https://amazon.com'

# Default Values
title = ''
price = 0.0
desc = ''

# Enter URL
url = input() 

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
r = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(r)
soup = bs(html, 'lxml')

# Get title.
title = soup.find("span", {"id": "productTitle"}).text.strip()

# Get price (as float).
# Scraped as string in format "$##.##", then converted.
if ((soup.find("span", {"class": "a-size-medium a-color-price offer-price a-text-normal"}))):
  price = float(soup.find("span", {"class": "offer-price"}).text[1:])
if ((soup.find("span", {"id": "price_inside_buybox"}))):
  price = soup.find("span", {"id": "price_inside_buybox"}).text.strip()
  price = price[1:]

# Get description from meta tag in header.
# Default description, in case there is none, or it was not scraped.
desc = soup.find("meta", {"name": "description"}).get("content")

# Get description from noscript tag.
# Some products have their descriptions listed in iframes, but they can be scraped
# from the <noscript> tags, which act as a fallback, if Javascript is disabled.
if (soup.find("script", {"id": "bookDesc_override_CSS"})):
  desc = soup.find("script", {"id": "bookDesc_override_CSS"}).next_sibling.next_sibling.text
  desc = remove_tags(desc).strip()

# Get description from unordered list.
# Scraped bulleted-list for text and concatenated to description.
if (soup.find("div", {"id": "feature-bullets"})):
  desc = ''
  features = soup.find("div", {"id": "feature-bullets"}).find_all("li", {"class": None})
  for f in features:
    desc += f.text.strip() + '\n'

if (soup.find)

# NOT DONE! NOT DONE! NOT DONE! NOT DONE!
# Get images (all, high-resolution)
#script = soup.find_all('script', type='text/javascript')[55].text[83:].strip()
#print(script[:6562])
#data = json.loads(script.text)
#urls = []
#image_num = 0

# Output
print(title)
print(price)
print(desc)

