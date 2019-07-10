# =============================================================================
# game.py
# This module defined the Game class and methods, including game behavior 
# and functionality of game mechanics
# =============================================================================

import sys
import time
import random
import math
import sqlite3
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
    
    self.current_question = 1
    self.number_of_questions = x


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
      return True

  def calculate_score(self, user_guess, time):
    MAX_SCORE = 10000
    MAX_EXACT_PERC = 0.01
    MAX_VERY_CLOSE_PERC = 0.2
    MAX_CLOSE_PERC = 0.4
    TIER_PENALTY = 1000  #points you instantly lose for being in a lower tier
    score = 0

    score_difference = abs(self.question_list[self.current_question - 1].getPrice() - user_guess)
    percentage = float((score_difference)/(self.question_list[self.current_question - 1].getPrice())) #gets percentage difference to real price
    if(percentage <= MAX_EXACT_PERC): # exact
      score = MAX_SCORE
      self.score_list.append(Score('EXACT', score, time))
      return self.score_list[self.current_question - 1]
    
    elif(percentage <= MAX_VERY_CLOSE_PERC ): # very close
      score =  int((MAX_SCORE - TIER_PENALTY) * (1 - percentage))
      self.score_list.append(Score('VERY CLOSE', score, time))
      return self.score_list[self.current_question - 1]

    elif(percentage <= MAX_CLOSE_PERC):#close
      score =  int((MAX_SCORE - (2 * TIER_PENALTY) ) * (1 - percentage))
      self.score_list.append(Score('CLOSE', score, time))
      return self.score_list[self.current_question - 1]

    else: #wrong
      score = 0
      self.score_list.append(Score('WRONG', score, time))
      return self.score_list[self.current_question - 1]
    
  def get_final_score(self):
    final_score = 0
    for score in self.score_list:
      final_score = final_score + score.get_score()
    return final_score

  def write_game(self, username, time_started):
    duration = int(time.time()- time_started)
    connection = sqlite3.connect('app.db')
    connection.execute("insert into games_played (username,duration,score) values (?, ?, ?);", (username, duration, self.get_final_score() ))
    connection.commit()
    connection.close()
        
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

