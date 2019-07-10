import unittest
import time
from objects.user import Player

class TestUser(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.player1 = Player('cornflakes', 'tothefloor')

  def test_password_Check(self):
    self.assertTrue(Player.password_Check('password1', 'password1'))
    self.assertFalse(Player.password_Check('password2', 'password3'))

  def test_length_check(self):
    self.assertTrue(Player.length_check('a'))
    self.assertTrue(Player.length_check('abcdefghijklmnopqrstuvwxyz'))
    self.assertFalse(Player.length_check('abcdef'))

  def test_check_username(self):
    self.assertTrue(Player.check_Username('test')) # Exists in db
    self.assertFalse(Player.check_Username('avocadotoast')) # Doesn't exist in db

  def test_get_top_five(self):
    self.assertEqual(len(Player.get_top_five()), 5)

if __name__ == '__main__':
  unittest.main()