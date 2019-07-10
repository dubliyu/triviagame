# =========================================================================== #
# scraper.py                                                                  #
# This module scraps a given URL for product information, i.e. name, price,   #
# description, and images.                                                    #
# =========================================================================== #
#
# NOTE: Only tested with Amazon.
#

from bs4 import BeautifulSoup as bs
from pathlib import Path
import shutil
import string
import lxml
import urllib.request
import urllib.error
import json
import re
import os
import time
import sys


_AMAZON = 'https://www.amazon.com'
TIMEOUT_TIME = 10 # seconds
MAX_RETRY = 3

# Folder names
_TEMP = 'temp/'
_IMG = 'img/'

# =========================================================================== #
#                             SYSTEM FUNCTIONS                                #
# =========================================================================== #

# Creates folder with name, if none exists
def create_Folder(name):
  if not os.path.exists(name):
    os.makedirs(name)

# Deletes folder with name, if it exists
def delete_Folder(name):
  if os.path.exists(name):
    shutil.rmtree(name)

# =========================================================================== #
#                         STRING FORMATTING FUNCTIONS                         #
# =========================================================================== #

# Removes HTML tags from a string.
def remove_HTML_tags(string):
  tag = re.compile(r'<[^>]+>')
  return tag.sub('', string)

# Formats a query to be used in a search.
def format_query(query):
  return query.replace(' ', '+').strip()

# =========================================================================== #
#                             SCRAPING FUNCTIONS                              #
# =========================================================================== #

# Checks if URL links to an Amazon webpage.
def is_Amazon_URL(url):
  return True if _AMAZON in url else False

# Checks if URL links to a Walmart webpage.
def is_Walmart_URL(url):
  return True if _WALMART in url else False

# Returns soup (HTML parsed by BeautifulSoup) from a URL.
def open_url(url):
  # Headers for server authentication
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
  req = urllib.request.Request(url, headers=headers)
  try:
    response = urllib.request.urlopen(req, timeout=TIMEOUT_TIME)
    if response.getcode() != 200:
      for i in range (0, MAX_RETRY):
        req = urllib.request.Request(url, headers=cls.headers)
        response = urllib.request.urlopen(req, timeout=TIMEOUT_TIME)
        if (response.getcode() == 200):
          break
        time.sleep(0.5) 
  except TimeoutError:
    print('Timeout occurred for ' + url)
    pass
  except (urllib.error.HTTPError, urllib.error.URLError):
    print('Error: Data not retrieved for ' + url)
    pass
  except:
    print('Exception occurred for ' + url)
    pass
  soup = bs(response.read(), 'lxml')
  return soup if (response.getcode() == 200) else ''

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
# NOTE: To use scrape functions, a parsed HTML file, or soup, must be passed. #
# Example:                                                                    #
#   >>> soup = open_url(url)                                                  #
#   >>> scrape_title(soup)                                                    #
#   Product Title ABC123 CATS???                                              #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #

# Returns title of product listing.
def scrape_title(soup):
  product_title = soup.find('span', {'id': 'productTitle'})
  return product_title.text.strip() if product_title else ''

# Returns price from product listing as a float.
def scrape_price(soup):
  # Prices can be presented differently based on the type of product.
  price1 = soup.find('span', {'class': 'a-size-medium a-color-price offer-price a-text-normal'})
  price2 = soup.find('span', {'id': 'price_inside_buybox'})
  price3 = soup.find('span', {'id': 'priceblock_ourprice'})
  price4 = soup.find('span', {'class': 'price-large'})

  if price1:
    return float(price1.text[1:])
  elif price2:
    return float(price2.text.strip()[1:])
  elif price3 and not price4:
    return float(price3.text.strip()[1:])
  elif price4:
    cents = price4.find_next_sibling('span', {'class': 'price-info-superscript'})
    if cents:
      return float(price4.text.strip() + '.' + cents.text.strip())
    else:
      return float(price4.text.strip() + '.99')
  else:
    return 0.0

# Returns description from product listing
def scrape_desc(soup):
  desc = ''

  # Get description from meta tag in header.
  # Default description, if no other information can be scraped.
  default_desc = soup.find('meta', {'name': 'description'})
  if default_desc:
    default_desc = default_desc.get('content')
  
  desc = soup.find('script', {'id': 'bookDesc_override_CSS'})
  features = soup.find('div', {'id': 'feature-bullets'})

  # Get description from <noscript> tag.
  # Some products have their descriptions listed in iframes, which cannot be scraped
  # from the HTML. However, they can be scraped from the <noscript> tag, 
  # which acts as a fallback, if Javascript is disabled.
  if desc:
    desc = desc.next_sibling.next_sibling.text
    desc = remove_HTML_tags(desc).strip()
    return desc

  # Get description from unordered list.
  # Scraped bulleted-list for text and concatenated to description.
  elif not desc and features:
    desc = ''
    features = features.find_all('li', {'class': None})
    for f in features:
      desc += f.text.strip() + '\n\n'
    return desc

  else:
    return default_desc

# Returns list of hi-res image URLs (as strings)
def scrape_Image_URLs(soup):
  img_urls = []
  img_num = 0

  img_script = soup.find('script', text = re.compile('ImageBlockATF'))

  # Check if script containing image URLs exists.
  if img_script:
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
        img_urls.append(data["imageGalleryData"][x]["mainUrl"])

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
        img_urls.append(data["colorImages"]["initial"][x]["hiRes"])
  
  return img_urls

# Downloads images to a temp folder
def download_images(title, img_urls):
  img_num = 0 # Number for naming files
  create_Folder(_TEMP)
  paths = []

  for img in img_urls:
    file_name = Path(_TEMP + title[:10] + '_' + str(img_num) + '.jpg')
    paths.append(file_name)
    img_num += 1
    try:
      response = urllib.request.urlopen(img, timeout=TIMEOUT_TIME)
      if response.getcode() != 200:
        for i in range (0, MAX_RETRY):
          req = urllib.request.Request(url, headers=cls.headers)
          response = urllib.request.urlopen(req, timeout=TIMEOUT_TIME)
          if (response.getcode() == 200):
            break
          time.sleep(0.5) 
    except TimeoutError:
      print('Timeout occurred. Image could not be retrieved from ' + img)
      pass
    except (urllib.error.URLError, urllib.error.HTTPError):
      print('Data could not be retrieved from ' + img)
      pass
    except:
      print('Exception occurred for' + img)
      continue
    file_name.write_bytes(response.read())
    time.sleep(1) # Delay between downloads
  return paths

# Returns a zip object containing the titles, URLs, and image URLs of results.
def get_search_results(query):
  MAX_RESULTS = 5 
  result_titles = []
  result_urls = []
  result_imgs = []
  query_url = _AMAZON + '/s?k=' + format_query(query)

  soup = open_url(query_url)

  results = soup.find_all('div', {'class': 's-result-item'})
  if not results:
    print('No results found.')
    return

  for i in range(0, MAX_RESULTS):
    title = results[i].find('h2')
    image = results[i].find('img')
    if not title or not image:
      break
    url = image.parent.parent
    if (not title or not image or not url):
      break
    result_titles.append(title.text.strip())
    result_imgs.append(image['src'])
    result_urls.append(_AMAZON + url['href'])
  
  # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
  # NOTE: results_data is a zip object, which can be understood as a          #
  # list of tuples, (title, url, image). To access data, create a list, and   #
  # assign it the zip object with list(). Use subscripting to access data.    #
  # Example:                                                                  #
  #   >>> listA = list(results_data)                                          #
  #   >>> listA[0]                                                            #
  #   (title, url, image)                                                     #
  #   >>> listA[0][0]                                                         #
  #   title                                                                   #
  # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
  results_data = zip(result_titles, result_imgs, result_urls)
  return results_data

# =========================================================================== #

# url = input()
# soup = open_url(url)
# title = scrape_title(soup)
# price = scrape_price(soup)
# print(title)
# print(price)
# print(scrape_desc(soup))
# img_urls = scrape_Image_URLs(soup)
# download_images(title, img_urls)
# query = input()
# get_search_results(query)
# delete_Folder(_TEMP)


