# =============================================================================
# game.py
# This module defined the Game class and methods, including game behavior 
# and functionality of game mechanics
# =============================================================================

import sys
import time
import random
import math
from question import Question
# from app import mywindow

class Game:
  MAX_QUESTIONS = 10
  current_question = 1
  number_of_questions = 0
  question_list = []
  score_list = []

  # def __init__(self):
  #   question_list = self.load_questions()

  def load_questions(self):
    qid_list = Question.get_question_ids()  #get a list of question ids, so we can remove one when it is used #TODO this will exentually be static for the session
    self.question_list.clear()
    self.score_list.clear()
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

  def calculate_score(self, user_guess, time):
    MAX_SCORE = 5000 

    MIN_SCORE_VERY_CLOSE = 2500
    MIN_SCORE_CLOSE = 500
    score = 0
    score_difference = abs(self.question_list[self.current_question - 1].getPrice() - user_guess)
    percentage = float((score_difference)/(self.question_list[self.current_question - 1].getPrice())) #gets percentage difference to real price
    print(f'Percentage difference to real score: {percentage}')
    if(percentage <= 0.01): # exact
      score = 5000
      self.score_list.append(Score('EXACT', score, time))
      return self.score_list[self.current_question - 1]
    
    elif(percentage <= 0.1 ): # very close
      score =  int(MIN_SCORE_VERY_CLOSE + (MAX_SCORE - MIN_SCORE_VERY_CLOSE)*(percentage * 10))
      self.score_list.append(Score('EXACT', score, time))
      return self.score_list[self.current_question - 1]

    elif(percentage <= 0.4):#close
      score =  int(MIN_SCORE_VERY_CLOSE + (MAX_SCORE - MIN_SCORE_VERY_CLOSE)*(percentage * 2.5))
      self.score_list.append(Score('EXACT', score, time))
      return self.score_list[self.current_question - 1]

    else: #wrong
      score = 0
      self.score_list.append(Score('EXACT', score, time))
      return self.score_list[self.current_question - 1]
    
  def get_final_score(self):
    final_score = 0
    for score in self.score_list:
      final_score = final_score + score.get_score()

    return final_score
        
class Score:

  def __init__(self, label, score, time):
    self.label = label
    self.score = score
    self.time = time

  def get_score(self):
    return self.score

  def get_label(self):
    return self.label

  def get_time(self):
    return self.time

if __name__ == '__main__':
  game = Game()

