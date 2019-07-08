# =============================================================================
# question.py
# This module defines the Question class and methods, including database I/O.
# =============================================================================

import sys
from pathlib import Path
import time
import random
import sqlite3
import re

class Question:
  # num_Questions = 0
  image_folder = 'img'

  name = 'Product'
  price = 0
  description = 'Enter description'
  default_path = 'img\\default.jpeg'
  img_path =  default_path
  qid = -1

  def __init__(self, name, price, description, img_path = False):
    self.setName(name)
    self.setPrice(price)
    self.setDescription(description)
    if img_path:
      self.setImagePath(img_path)
    else:
      self.qid = self.addQuestion(self.getName(),self.getPrice(),self.getDescription(),self.getImagePath()) #TODO this automatically pushes questions to DB when no img path exists, maybe change?
      self.setImagePath(self.generateImagePath())
      self.updateQuestion()

  def setName(self,name):
    self.name = str(name)

  def getName(self):
    return self.name

  # Sets price of question item
  def setPrice(self, price):
    self.price = int(re.sub('[^0-9]', '', str(price))) #replaces all non-digits with ''

  # Returns price of question item
  def getPrice(self):
    return self.price

  def setDescription(self,description):
    self.description =  str(description)

  def getDescription(self):
    return self.description

  #generates the path of an image of the product
  def generateImagePath(self):
    new_path = self.image_folder + '\\' +  f'{self.qid:>06}.jpeg' #6 character filename with padding
    return new_path #6 character filename with padding
    
  def setImagePath(self,img_path):
    self.img_path = str(img_path)
  
  #get the path to the image of the product
  def getImagePath(self):
    file = Path(self.img_path)
    if file.is_file():
      return self.img_path
    else:
      return self.default_path

  def getID(self):
    return self.qid
  
  #### TODO Validation of input

  #### Database stuff:
  @staticmethod
  def totalQuestions(): #returns total number of questions in the database
    connection = sqlite3.connect('app.db')
    total = connection.execute("select count(*) from questions;").fetchone()[0]
    connection.close()
    # print(f'Total is : {total}')
    return total

  @staticmethod
  def addQuestion(name, price, description, img_path):
    connection = sqlite3.connect('app.db')
    connection.execute("insert into questions (name, price, description, image) values (?, ?, ?, ?);", (name, price, description, img_path))
    connection.commit()
    qid = connection.execute("select last_insert_rowid()").fetchone()[0]
    connection.close()
    return qid

  @staticmethod
  def removeQuestion(qid):
    connection = sqlite3.connect('app.db')
    connection.execute("delete from questions where qid=?;", (qid,))
    connection.commit()
    connection.close()
    
  @staticmethod
  def createQuestion(qid_input = 0):
    connection = sqlite3.connect('app.db')
    c = connection.cursor()
    c.execute("select * from questions where qid=?;", (qid_input,))
    question = c.fetchone()
    connection.close()
    return Question(question[1], question[2], question[3], question[4])

  def loadQuestion(self): #pulls question from database and replaces local values
    connection = sqlite3.connect('app.db')
    c = connection.cursor()
    c.execute("select * from questions where qid=?;", (self.getID(),))
    question = c.fetchone()
    connection.close()
    self.setName(question[1])
    self.setPrice(question[2])
    self.setDescription(question[3])
    self.setImagePath(question[4])

  def updateQuestion(self): #pushes local (changed) values to database
    connection = sqlite3.connect('app.db')
    connection.execute("update questions set (name, price, description, image)=(?, ?, ?, ?) where qid=?;",(self.getName(), self.getPrice(), self.getDescription(), self.img_path, self.qid))
    connection.commit()
    connection.close()

  @staticmethod
  def get_question_ids(): #returns a list of all qids current in database
    qid_list = []
    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()
    qid_selection = cursor.execute("select qid from questions;").fetchall()
    connection.close()
    for x in range(len((qid_selection))): #TODO this can be cleaned up.  just converts 'list of tuples containing 1 int into list of ints
      qid_list.append(qid_selection[x][0])
    return qid_list


if __name__ == '__main__': #Manually inserting a question (dev tool)
  add_question_input = input('Add a question? (Y/N):')
  while add_question_input == 'Y' or add_question_input == 'y':
    name_input  = input('Name: ')
    price_input = input('Price: ')
    description_input = input('Description:')
    question = Question(name_input,price_input,description_input,None)
    print('Please place image file at ' + question.getImagePath())
    print(f'\nTotal number of questions so far:{Question.totalQuestions()}' )

    add_question_input = input('Add another question? (Y/N):')
    # Question.
  test_list = Question.get_question_ids()
  qid_list_selection = input('Show list of QIDs (Y/N): ')
  if qid_list_selection == 'Y' or qid_list_selection == 'y':
    print(test_list)

  x = 1
  delete_questions = input(f'[{x}/10] Delete all question: (Y/N): ')

  while delete_questions == 'Y' or delete_questions == 'y':
    x = x + 1
    if x > 10:
      for y in test_list:
        Question.removeQuestion(y)
        print(f'attemped to remove question {y}')
      break
    else:
      delete_questions = input(f'[{x}/10] Delete all questions?: (Y/N): ')
