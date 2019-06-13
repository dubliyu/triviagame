# question.py
#  Question getters/setter and Database i/o
import sys
import time
import random
import sqlite3


class Question:
  # num_Questions = 0
  image_folder = 'img'
  qid = -1

  def __init__(self, name, price, description, img_path):
    self.setName(name)
    self.setPrice(price)
    self.setDescription(description)
    if img_path:
      self.setImagePath(img_path)
    else:
      self.setImagePath(self.generateImagePath())
    self.qid = self.addQuestion(name,price,description,self.getImagePath()) #TODO this automatically pushes questions to DB when they are created, maybe change?
  
  def setName(self,name):
    self.name = name

  def getName(self):
    return self.name

  # Sets price of question item
  def setPrice(self, price):
    self.price = price

  # Returns price of question item
  def getPrice(self):
    return self.price

  def setDescription(self,description):
    self.description =  description

  def getDescription(self):
    return self.description

  #generates the path of an image of the product
  def generateImagePath(self):
    question_id = random.randint(1,999999) #TODO make this either unique or equal to qid in questions table
    return self.image_folder + '\\' +  f'{question_id:>06}.jpg' #6 character filename with padding
    
  def setImagePath(self,img_path):
    self.img_path = img_path
  
  #get the path to the image of the product
  def getImagePath(self):
    return self.img_path

  def getID(self):
    return self.qid
  
  #### TODO Validation of input

  #### Database stuff:
  @staticmethod
  def totalQuestions(): #returns total number of questions in the database
    connection = sqlite3.connect('app.db')
    total = connection.execute("select count(*) from questions;").fetchone()[0]
    connection.close()
    return total;

  @staticmethod
  def addQuestion(name, price, description, img_path):
    connection = sqlite3.connect('app.db')
    connection.execute("insert into questions (name, price, description, image) values (?, ?, ?, ?);", (name, price, description, img_path))
    connection.commit()
    qid = connection.execute("select last_insert_rowid()").fetchone()
    connection.close()
    return qid;

  @staticmethod
  def removeQuestion(qid):
    connection = sqlite3.connect('app.db')
    connection.execute("delete from questions where qid=?;", (qid))
    connection.commit()
    connection.close()
    

  @staticmethod
  def createQuestion(qid = 0):
    connection = sqlite3.connect('app.db')
    c = connection.cursor()
    c.execute("select * from questions where qid=?", (qid))
    question = c.fetchall()
    connection.close()
    return Question(question[1], question[2], quesiton[3], question[4])

  def loadQuestion(self): #pulls question from database and replaces local values
    connection = sqlite3.connect('app.db')
    c = connection.cursor()
    c.execute("select * from questions where qid=?", (self.getID()))
    question = c.fetchall()
    connection.close()
    self.setName(question[1])
    self.setPrice(question[2])
    self.setDescription(question[3])
    self.setImagePath(question[4])

  def updateQuestion(self): #pushes local (changed) values to database
    connection = sqlite3.connect('app.db')
    connection.execute("update questions set (name, price, description, image) values (?, ?, ?, ?) where qid=?;", (self.getName(),
    self.getPrice(),
    self.getDescription(),
    self.getImagePath(),
    self.qid))
    connection.commit()
    connection.close()
    return




if __name__ == '__main__': #Manually inserting a question (dev tool)
  add_question_input = input('Add a question? (Y/N):')
  while add_question_input == 'Y' or add_question_input == 'y':
    name_input  = input('Name: ')
    price_input = input('Price: ')
    description_input = input('Description:')
    question = Question(name_input,price_input,description_input,None)
    # path_input = generatePath()
    print('Please place image file at ' + question.getImagePath())
    print(f'\nTotal number of questions so far:{Question.totalQuestions()}' )

    add_question_input = input('Add another question? (Y/N):')
    # Question.


  #input("Launch the ui?")