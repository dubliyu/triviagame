import unittest
import time
from game import Game, Score

class TestGame(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.game = Game()
    cls.Score1 = Score('name', 2222, time)

  def test_load_questions(self):
    # Test that questions are being loaded into question_list
    self.game.load_questions()
    self.assertGreater(len(self.game.question_list), 0)

  def test_get_question(self):
    # Assert question is not NoneType
    self.assertEqual(self.game.get_question(), None)

  def test_next_question(self):
    # Assert that index in question_list is incremented by 1
    start = self.game.current_question
    self.game.next_question()
    next = self.game.current_question

    self.assertNotEqual(start, next)
    self.assertEqual(start + 1, next)

  def test_get_score(self):
    self.assertEqual(self.Score1.get_score(), 2222)

  def test_get_label(self):
    self.assertEqual(self.Score1.get_label(), 'name')

  def test_get_time(self):
    self.assertAlmostEqual(self.Score1.get_time(), time)

if __name__ == '__main__':
  unittest.main()