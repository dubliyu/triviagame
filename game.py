# game.py
# Game class and methods
# Defines behavior and functionality of game mechanics

import sys
import time

#class Game:

  # Creates a set of 10 questions from database
  # def generate_Questions()

# Counts down the time for a player to guess
def countdown():
  TIME = 30 #seconds
  for t in range(TIME, 0, -1):
    print(t)
    time.sleep(1) # Delay 1 second