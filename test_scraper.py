import unittest
import scraper

class TestScraper(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    print('setupClass')
    book_soup

  def test_is_Amazon_URL(self):
    print('Test: is_Amazon_URL()')
    self.assertTrue(scraper.is_Amazon_URL('https://amazon.com/'))
    self.assertFalse(scraper.is_Amazon_URL('https://ama'))
    self.assertFalse(scraper.is_Amazon_URL('https://youtube.com/'))

  def test_open_URL(self):
    print('Test: open_URL()')
    self.

if __name__ == '__main__':
  unittest.main()