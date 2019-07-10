from bs4 import BeautifulSoup as bs
import unittest
from unittest.mock import patch, MagicMock
import scraper
import urllib.request
import lxml
import time

class TestScraper(unittest.TestCase):
  # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
  # urls = ['https://www.amazon.com/dp/1945056088/',
  #         'https://www.amazon.com/dp/B01AHGOMFU/',
  #         'https://www.amazon.com/dp/B00G4GQFMG/',
  #         'https://www.amazon.com/dp/0762444142/',
  #         'https://www.amazon.com/dp/B07PWJXXJ4/',
  #         'https://www.amazon.com/dp/045149492X/']
  # soups = []

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


  # @classmethod
  # def setUpClass(cls):
  #   for url in cls.urls:
  #     req = urllib.request.Request(url, headers=cls.headers)
  #     response = urllib.request.urlopen(req)
  #     while response.getcode() != 200:
  #       req = urllib.request.Request(url, headers=cls.headers)
  #       response = urllib.request.urlopen(req)
  #       time.sleep(0.5) 
  #     response = urllib.request.urlopen(req)
  #     cls.soups.append(bs(response.read(), 'lxml'))
  #     time.sleep(0.5) # Delay between page requests

  # def test_is_Amazon_URL(self):
  #   self.assertTrue(scraper.is_Amazon_URL('https://amazon.com/'))
  #   self.assertFalse(scraper.is_Amazon_URL('https://ama'))
  #   self.assertFalse(scraper.is_Amazon_URL('amazon'))
  #   self.assertFalse(scraper.is_Amazon_URL('https://youtube.com/'))

  # def test_scrape_title(self):
  #   self.assertEqual(scraper.scrape_title(self.soups[0]), 'People of Walmart.com Adult Coloring Book: Rolling Back Dignity')
  #   self.assertEqual(scraper.scrape_title(self.soups[1]), 'Accoutrements Lucky Yodelling Pickle: Ornament Standard')
  #   self.assertEqual(scraper.scrape_title(self.soups[2]), 'Prank Pack Nap Sack')
  #   self.assertEqual(scraper.scrape_title(self.soups[3]), 'Dancing with Jesus: Featuring a Host of Miraculous Moves')
  #   self.assertEqual(scraper.scrape_title(self.soups[4]), 'Mother Earth\'s Plantasia')
  #   self.assertEqual(scraper.scrape_title(self.soups[5]), 'How to Talk to Your Cat About Gun Safety: And Abstinence, Drugs, Satanism, and Other Dangers That Threaten Their Nine Lives')

  # def test_scrape_price(self):
  #   self.assertNotEqual(scraper.scrape_price(self.soups[0]), 0.0)
  #   self.assertNotEqual(scraper.scrape_price(self.soups[1]), 0.0)
  #   self.assertNotEqual(scraper.scrape_price(self.soups[2]), 0.0)
  #   self.assertNotEqual(scraper.scrape_price(self.soups[3]), 0.0)
  #   self.assertNotEqual(scraper.scrape_price(self.soups[4]), 0.0)
  #   self.assertNotEqual(scraper.scrape_price(self.soups[5]), 0.0)

  # def test_scrape_Image_URLs(self):
  #   for soup in self.soups:
  #     self.assertNotEqual(scraper.scrape_Image_URLs(soup), [])

  # def test_get_search_results(self):
  #   queries = ['harry potter', 'crickets', 'sonic movie 2019', 'us 2019', 'golden whale on mars dancing to the Beatles wearing a sombrero cause it can']

  #   z1 = scraper.get_search_results(queries[0])
  #   z2 = scraper.get_search_results(queries[1])
  #   z3 = scraper.get_search_results(queries[2])
  #   z4 = scraper.get_search_results(queries[3])
  #   z5 = scraper.get_search_results(queries[4])

  #   l1 = list(z1)
  #   l2 = list(z2)
  #   l3 = list(z3)
  #   l4 = list(z4)
  #   l5 = list(z5)

  #   self.assertEqual(len(l1[0]), len(l1[1]), len(l1[2]))
  #   self.assertEqual(len(l2[0]), len(l2[1]), len(l2[2]))
  #   self.assertEqual(len(l3[0]), len(l3[1]), len(l3[2]))
  #   self.assertEqual(len(l4[0]), len(l4[1]), len(l4[2]))

if __name__ == '__main__':
  unittest.main()
