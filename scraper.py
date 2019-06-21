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
from pathlib import Path
import shutil
import string
import lxml
import urllib.request
import json
import re
import os
import time
import sys

_AMAZON = 'https://amazon.com'
_WALMART = 'https://walmart.com'

_TEMP = 'temp/'
_IMG = 'img/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

class amazon_scraper:
  soup = ''
  title = ''
  price = 0.0
  desc = ''
  img_urls = []

  def __init__(self, url):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    self.soup = bs(response.read(), 'lxml')
    self.scrape()

  # Scrapes title from product listing
  def scrape_title(self):
    product_title = self.soup.find('span', {'id': 'productTitle'})
    self.title = product_title.text.strip() if product_title else ''

  # Returns product
  def get_title(self):
    return self.title

  # Scrapes price from product listing
  def scrape_price(self):
    price1 = self.soup.find('span', {'class': 'a-size-medium a-color-price offer-price a-text-normal'})
    price2 = self.soup.find('span', {'id': 'price_inside_buybox'})
    if (not price1 and not price2):
      return
    self.price = float(price1.text[1:]) if price1 else float(price2.text.strip()[1:])

  # Returns product price
  def get_price(self):
    return self.price

  # Scrapes description from product listing
  def scrape_desc(self):
    desc = ''

    # Get description from meta tag in header.
    # Default description, if no other information can be scraped.
    default_desc = self.soup.find('meta', {'name': 'description'}).get('content')

    # Get description from <noscript> tag.
    # Some products have their descriptions listed in iframes, which cannot be scraped
    # from the HTML. However, they can be scraped from the <noscript> tag, 
    # which acts as a fallback, if Javascript is disabled.
    desc = self.soup.find('script', {'id': 'bookDesc_override_CSS'})
    if desc:
      desc = desc.next_sibling.next_sibling.text
      desc = remove_HTML_tags(desc).strip()
      self.desc = desc

    # Get description from unordered list.
    # Scraped bulleted-list for text and concatenated to description.
    elif not desc:
      desc = ''
      features = self.soup.find('div', {'id': 'feature-bullets'}).find_all('li', {'class': None})
      for f in features:
        desc += f.text.strip() + '\n'
      self.desc = desc

    else:
      self.desc = default_desc

  # Returns product description
  def get_desc(self):
    return self.desc

  # Returns list of image URLs (as strings)
  def get_hiRes_Image_URLs(self):
    img_num = 0

    img_script = self.soup.find('script', text = re.compile('ImageBlockATF'))
    #print(img_script.text) if img_script else print('Script not found')

    if 'imageGalleryData' in img_script.text:
      # Format string to valid json format
      start = img_script.text.index('var data = ') + len('var data = ')
      end = img_script.text[start:].index('};') + 1
      img_json = img_script.text[start:].strip()
      img_json = img_json[:end].strip()
      img_json = img_json.replace('\'', '"')
      
      # audibleData is an arbitrary variable in the script.
      # It must be changed to a string for json to be valid.
      img_json = img_json.replace('audibleData,', '"audibleData",')

      data = json.loads(img_json)
      img_num = len(data["imageGalleryData"])
      for x in range(0, img_num):
        self.img_urls.append(data["imageGalleryData"][x]["mainUrl"])

    elif 'colorImages' in img_script.text:
      # Format string to valid json format
      start = img_script.text.index('var data = ') + len('var data = ')
      end = img_script.text[start:].index('};') + 1
      img_json = img_script.text[start:].strip()
      img_json = img_json[:end].strip()
      img_json = img_json.replace('\'', '"')

      data = json.loads(img_json)
      img_num = len(data["colorImages"]["initial"])
      for x in range(0, img_num):
        self.img_urls.append(data["colorImages"]["initial"][x]["hiRes"])

  # Downloads images to a temp folder
  def download_images(self):
    img_num = 1
    self.get_hiRes_Image_URLs()

    # Create temp folder, if none exists
    if not os.path.exists(_TEMP):
      os.makedirs(_TEMP)

    for img in self.img_urls:
      file_name = Path(_TEMP + self.title[:10] + '_' + str(img_num) + '.jpg')
      img_num += 1
      response = urllib.request.urlopen(img)
      file_name.write_bytes(response.read())
      time.sleep(1) # Scrape delay

  def scrape(self):
    self.scrape_title()
    self.scrape_price()
    self.scrape_desc()
    self.download_images()

def is_Amazon_URL(url):
  return True if _AMAZON in url else False

def is_Walmart_URL(url):
  return True if _WALMART in url else False

# Removes HTML tags from a string.
def remove_HTML_tags(string):
  tag = re.compile(r'<[^>]+>')
  return tag.sub('', string)

# Deletes temp folder, if it exists
def delete_temp():
  if os.path.exists(_TEMP):
    shutil.rmtree(_TEMP)

# Formats a query to a 
def format_query(query):
  return query.replace(' ', '+').strip()

class results_scraper():
  MAX_RESULTS = 5
  product_titles = []
  product_urls = []
  img_urls = []

  def __init__(self, query):
    r = urllib.request.Request(_AMAZON + '/s?k=' + format_query(query), headers=headers)
    html = urllib.request.urlopen(r)
    soup = bs(html, 'lxml')

  # Returns list of product titles from search results.
  def get_titles(self):
    return self.product_titles

  # Returns list of URLs to products from search results.
  def get_urls(self):
    return self.product_urls

  # Returns list of URLs to image thumbnails from search results.
  def get_imgs(self):
    return self.img_urls

def get_search_results(query):
  MAX_RESULTS = 5 
  result_titles = []
  result_urls = []
  result_imgs = []
  query = format_query(query)
  r = urllib.request.Request(_AMAZON + '/s?k=' + query)
  html = urllib.request.urlopen(r)
  soup = bs(html, 'lxml')

  results = soup.find_all('div', {'class': 's-result-item'})
  if not results:
    print('No results found.')
    return

  for i in range(0, MAX_RESULTS):
    title = results[i].find('h2')
    image = results[i].find('img')
    url = image.parent.parent
    if (not title or not image or not url):
      break
    result_titles.append(title.text.strip())
    result_imgs.append(image['src'])
    result_urls.append(_AMAZON + url['href'])

#url = input() 
#scraper = amazon_scraper(url)
query = input()
get_search_results(query)

# delete_temp()


