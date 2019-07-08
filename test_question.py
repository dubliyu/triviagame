import unittest
import question
from question import Question
import sys
from pathlib import Path
import time
import random


class TestScraper(unittest.TestCase):

  # @classmethod
  # def setUpClass(cls):

  def setUp(self):
    self.q1 = Question('towel', '9999.99', 'don\'t forget to bring a', None)

  # def tearDown(self):
  
  def test_setName(self):
    self.assertNotEqual(self.q1.name, 'towels')
    self.q1.setName('towels')
    self.assertEqual(self.q1.name, 'towels')

  def test_getName(self):
    self.assertEqual(self.q1.name, 'towel')
    self.q1.name = 'towels'
    self.assertEqual(self.q1.getName(), 'towels')

  def test_setPrice(self):
    self.assertEqual(self.q1.price, 999999)
    self.q1.setPrice(1.22)
    self.assertEqual(self.q1.price, 122)

  def test_getPrice(self):
    self.assertEqual(self.q1.getPrice(), 999999)
    self.q1.price = 122
    self.assertEqual(self.q1.getPrice(), 122)

  def test_setDescription(self):
    self.assertEqual(self.q1.description, 'don\'t forget to bring a')
    self.q1.setDescription('this wasn\'t a reference probably')
    self.assertEqual(self.q1.description, 'this wasn\'t a reference probably')

  def test_getDescription(self):
    self.assertEqual(self.q1.getDescription(), 'don\'t forget to bring a')
    self.q1.description = 'this wasn\'t a reference probably'
    self.assertEqual(self.q1.getDescription(), 'this wasn\'t a reference probably')

  def test_totalQuestions(self):
    numQ = Question.totalQuestions()
    self.assertNotEqual(numQ, 0)

  def test_get_question_ids(self):
    self.assertNotEqual(Question.get_question_ids(), [])
    # print(Question.get_question_ids())
    


if __name__ == '__main__':
  unittest.main()
  