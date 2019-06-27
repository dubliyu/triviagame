from bs4 import BeautifulSoup as bs
import unittest
import scraper
import urllib.request
import lxml
import time

class TestScraper(unittest.TestCase):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
  urls = ['https://www.amazon.com/dp/1945056088/',
          'https://www.amazon.com/dp/B01AHGOMFU/',
          'https://www.amazon.com/dp/B00G4GQFMG/',
          'https://www.amazon.com/dp/0762444142/',
          'https://www.amazon.com/dp/B07PWJXXJ4/',
          'https://www.amazon.com/dp/045149492X/']
  soups = []

  @classmethod
  def setUpClass(cls):
    for url in cls.urls:
      req = urllib.request.Request(url, headers=cls.headers)
      response = urllib.request.urlopen(req)
      while response.getcode() != 200:
        req = urllib.request.Request(url, headers=cls.headers)
        response = urllib.request.urlopen(req)
        time.sleep(0.5) 
      response = urllib.request.urlopen(req)
      cls.soups.append(bs(response.read(), 'lxml'))
      time.sleep(0.5) # Delay between page requests

  def test_is_Amazon_URL(self):
    self.assertTrue(scraper.is_Amazon_URL('https://amazon.com/'))
    self.assertFalse(scraper.is_Amazon_URL('https://ama'))
    self.assertFalse(scraper.is_Amazon_URL('amazon'))
    self.assertFalse(scraper.is_Amazon_URL('https://youtube.com/'))

  def test_open_URL(self):
    for i in range(0, len(self.urls)):
      self.assertEqual(scraper.open_url(self.urls[i]), self.soups[i])
      time.sleep(0.5)

  def test_scrape_title(self):
    self.assertEqual(scraper.scrape_title(self.soups[0]), 'People of Walmart.com Adult Coloring Book: Rolling Back Dignity')
    self.assertEqual(scraper.scrape_title(self.soups[1]), 'Accoutrements Lucky Yodelling Pickle: Ornament Standard')
    self.assertEqual(scraper.scrape_title(self.soups[2]), 'Prank Pack Nap Sack')
    self.assertEqual(scraper.scrape_title(self.soups[3]), 'Dancing with Jesus: Featuring a Host of Miraculous Moves')
    self.assertEqual(scraper.scrape_title(self.soups[4]), 'Mother Earth\'s Plantasia')
    self.assertEqual(scraper.scrape_title(self.soups[5]), 'How to Talk to Your Cat About Gun Safety: And Abstinence, Drugs, Satanism, and Other Dangers That Threaten Their Nine Lives')

  def test_scrape_price(self):
    self.assertAlmostEqual(scraper.scrape_price(self.soups[0]), 10.79)
    self.assertAlmostEqual(scraper.scrape_price(self.soups[1]), 12.55)
    self.assertAlmostEqual(scraper.scrape_price(self.soups[2]), 7.99)
    self.assertAlmostEqual(scraper.scrape_price(self.soups[3]), 10.68)
    self.assertAlmostEqual(scraper.scrape_price(self.soups[4]), 22.98)
    self.assertAlmostEqual(scraper.scrape_price(self.soups[5]), 8.23)

  def test_scrape_desc(self):
    for url in self.urls:
      self.assertNotEqual(scraper.scrape_desc(url), None)

if __name__ == '__main__':
  unittest.main()