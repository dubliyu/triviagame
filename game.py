# =============================================================================
# game.py
# This module defined the Game class and methods, including game behavior 
# and functionality of game mechanics
# =============================================================================

import sys
import time
import random
from question import Question
# from app import mywindow

class Game:
  MAX_QUESTIONS = 10
  current_question = 1
  number_of_questions = 0
  question_list = []

  # def __init__(self):
  #   question_list = self.load_questions()

  def load_questions(self):
    qid_list = Question.get_question_ids()  #get a list of question ids, so we can remove one when it is used #TODO this will exentually be static for the session
    self.question_list.clear()
    for x in range(self.MAX_QUESTIONS):#donot exceed max questions
      if len(qid_list) == 0: #quit if not enough questions to populate
        print('Ran out of questions to add!')
        break
      else:
        qid = random.choice(qid_list)
        self.question_list.append(Question.createQuestion(qid))
        qid_list.remove(qid)
        print (f'Loaded Q{x+1} - Name: {self.question_list[x].getName()}')
    
    self.current_question = 1
    self.number_of_questions = x
    print(f'Loaded a total of {x} questions.')

  def get_question(self):
    if self.current_question <= self.number_of_questions:
      return self.question_list[self.current_question-1]
    else:
      return None
  # Calculates the score of a user guess
  # def calculate_score(guess):
    # if guess / question_list[current_question].getPrice()

  def next_question(self):
    if self.current_question >= self.number_of_questions:
      return False
    else:
      self.current_question = self.current_question + 1
      print(f'Current question is now {self.current_question} out of {self.number_of_questions}')
      return True

if __name__ == '__main__':
  game = Game()

  # app = QtWidgets.QApplication([])
  # w = mywindow().GamePage
  # #window.setGeometry(0, 0, 500, 300)
  # w.setWindowTitle("Game Example (Testing)")
  # w.show()
  # sys.exit(app.exec_())
  #   # game.load_questions()
    
 
