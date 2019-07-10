from bs4 import BeautifulSoup as bs
import unittest
from unittest.mock import patch, MagicMock
import scraper
import urllib.request
import lxml
import time

class TestScraper(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    pass

  def test_open_url(self):
    with patch('scraper.open_url') as mock_open:
      url1 = 'https://www.amazon.com/dp/B07GQ83P9L/'
      url2 = 'https://www.amazon.com/cornflakes'

      mock_response = mock_open.return_value
      mock_response.read.return_value = ''

      result = scraper.open_url(url2).read()

      mock_open.assert_called_with(url2)
      self.assertEqual(result, '')

      mock_response.read.return_value = '<html></html>'
      result = scraper.open_url(url1).read()
      self.assertNotEqual(result, '')

  def test_is_Amazon_URL(self):
    self.assertTrue(scraper.is_Amazon_URL('https://www.amazon.com/'))
    self.assertFalse(scraper.is_Amazon_URL('https://ama'))
    self.assertFalse(scraper.is_Amazon_URL('amazon'))
    self.assertFalse(scraper.is_Amazon_URL('https://youtube.com/'))

  def test_scrape_title(self):
    soup_title = bs('<html><span id="productTitle">Cornflakes tho</span></html>', 'lxml')
    self.assertEqual(scraper.scrape_title(soup_title), 'Cornflakes tho')

    soup_title = bs('', 'lxml')
    self.assertEqual(scraper.scrape_title(soup_title), '')

    soup_title = bs('<html></html>', 'lxml')
    self.assertEqual(scraper.scrape_title(soup_title), '')

  def test_scrape_price(self):
    soup_price = bs('', 'lxml')
    self.assertEqual(scraper.scrape_price(soup_price), 0.0)

    soup_price = bs('<html></html>', 'lxml')
    self.assertEqual(scraper.scrape_price(soup_price), 0.0)

    soup_price = bs('<html><span class="a-size-medium a-color-price offer-price a-text-normal">$9.99</span></html>', 'lxml')
    self.assertEqual(scraper.scrape_price(soup_price), 9.99)

    soup_price = bs('<html><span id="price_inside_buybox">$4.26</span></html>', 'lxml')
    self.assertEqual(scraper.scrape_price(soup_price), 4.26)

    soup_price = bs('<html><span id="priceblock_ourprice">$2.22</span></html>', 'lxml')
    self.assertEqual(scraper.scrape_price(soup_price), 2.22)

    soup_price = bs('<html><span class="price-large">99</span><span class="price-info-superscript">19</span></html>', 'lxml')
    self.assertEqual(scraper.scrape_price(soup_price), 99.19)

if __name__ == '__main__':
  unittest.main()