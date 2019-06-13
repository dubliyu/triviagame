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

  # Creates a set of questions from the database
  # DB Stuff
  # def load_Questions():
  #   srand()
  #   rand()
  #   question_list.append()

  # Calculates the score of a user guess
  # def calculate_Score(guess):
    #if guess / question_list[current_question].getPrice()

  # def next_Question():
    # current_question + 1