# game.py
# Game class and methods
# Defines behavior and functionality of game mechanics

import sys
import time
import random
from question import Question

class Game:
  MAX_QUESTIONS = 10
  current_question = 0
  question_list = []

  def __init__(self):
    question_list = self.load_questions()

  def load_questions(self):
    qid_list = Question.get_question_ids() #get a list of question ids, so we can remove one when it is used #TODO this will exentually be static for the session
    for x in range(self.MAX_QUESTIONS):#donot exceed max questions
      if len(qid_list) == 0: #quit if not enough questions to populate
        print('Ran out of questions')
        break
      qid = random.choice(qid_list)
      self.question_list.append(Question.createQuestion(qid))
      qid_list.remove(qid)
      print (f'{x+1} - Added {self.question_list[x].getName()}')
    


  # Calculates the score of a user guess
  # def calculate_score(guess):
    # if guess / question_list[current_question].getPrice()

  def next_Question():
    current_question + 1

if __name__ == '__main__':
  game = Game()
  # game.load_questions()
  
 
