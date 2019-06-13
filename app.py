# app.py
# Main function

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QLabel
from window import Ui_MainWindow
from threading import Thread, Timer, currentThread
from user import *
import re
import time
import sys
import user
from game import Game

# One Main Window, Multiple QStackedWidgets
class Main_Window(QtWidgets.QMainWindow):
  #Variables
  next_question_pushed = False
  game_instance = Game()
  timer_thread  = Thread()
  timer_thread.start()

  def __init__(self):
    super(Main_Window, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
  
    # Start Page Buttons
    self.ui.pushButton.clicked.connect(self.LoginPage)
    self.ui.pushButton_2.clicked.connect(self.RegisterPage)

    # Login Page Buttons
    self.ui.pushButton_3.clicked.connect(self.passoff_login)
    self.ui.pushButton_4.clicked.connect(self.StartPage)
    
    # Register Page Buttons
    self.ui.pushButton_8.clicked.connect(self.passoff_register)
    self.ui.pushButton_7.clicked.connect(self.StartPage)

    self.ui.pushButton_10.clicked.connect(self.PlayerMainMenu)

    # Player Main Menu Buttons
    self.ui.pushButton_12.clicked.connect(self.GamePage)
    self.ui.pushButton_13.clicked.connect(self.RecordsPage)

    # Game buttons
    self.ui.pushButton_9.clicked.connect(self.next_question_button)

    #Score Page buttons
    self.ui.pushButton_17.clicked.connect(self.PlayerMainMenu)

    # Records Buttons
    self.ui.pushButton_18.clicked.connect(self.PlayerMainMenu)

    # Leaderboard Buttons
    self.ui.pushButton_19.clicked.connect(self.PlayerMainMenu)

    self.ui.lcdNumber.display(30)


  # Passover control flow login to main menu
  def passoff_login(page):
    # Get input data
    username = page.ui.lineEdit.text()
    password = page.ui.lineEdit_2.text()

    # Validate
    if Player.length_check(username) or Player.length_check(password):
      show_error(page, "Credentials have invalid length,")
      page.ui.lineEdit_2.setText("")
    elif Player.alpha_check(username) or Player.alpha_check(password):
      show_error(page, "Only alpha numeric usernames/passwords allowed.")
      page.ui.lineEdit_2.setText("")
      page.ui.lineEdit.setText("")
    else:
      # Create user obj
      page.user_obj = Player(username, password)
      if page.user_obj.is_logged_in:
        page.PlayerMainMenu()
      else:
        # Bad login
        show_error(page, "Invalid Username/password combination.")
        page.ui.lineEdit_2.setText("")

  # Passover control flow from register to login
  def passoff_register(page):
    # Get input data
    username = page.ui.lineEdit_3.text()
    password = page.ui.lineEdit_4.text()
    re_password = page.ui.lineEdit_5.text()

    # Validate
    if Player.length_check(username) or Player.length_check(password) or Player.length_check(re_password):
      show_error(page, "Credentials have invalid length.")
      page.ui.lineEdit_4.setText("")
      page.ui.lineEdit_5.setText("")
    elif Player.alpha_check(username) or Player.alpha_check(password):
      show_error(page, "Only alpha numeric usernames/passwords allowed.")
      page.ui.lineEdit_4.setText("")
      page.ui.lineEdit_5.setText("")
    elif Player.check_Username(username):
      show_error(page, "Username is taken.")
      page.ui.lineEdit_3.setText("")
      page.ui.lineEdit_4.setText("")
      page.ui.lineEdit_5.setText("")
    else:
      # insert into user
      Player.add_User(username, password)
      page.StartPage()

  def start_timer(self):
    self.timer_thread = Thread(target = self._countdown)
    self.timer_thread.running = True
    self.timer_thread.start()

  def _countdown(self):
    TIME = 30 #seconds
    count = TIME
    running_thread = currentThread()
    while getattr(running_thread, "running", True) and count >= 0:
      self.ui.lcdNumber.display(count)
      time.sleep(1)
      count = count - 1
    #   print(f'{count} seconds left!')
    # print('Timer stopped!')

  def stop_timer(self): #TODO stop the timer when app closes
    self.timer_thread.running = False
    self.timer_thread.join()

  def next_question_button(self):
    if self.next_question_pushed == False: #if pushing submit button for first time
      self.next_question_pushed = True
      self.stop_timer()
      self.display_score()
    else:
      self.ui.lineEdit_6.setText('')
      if self.game_instance.next_question() is False: #if the last question has been reached, show score page
        self.next_question_pushed = False
        self.ScorePage()
      else:
        self.load_current_question()
        self.next_question_pushed = False

  def display_score(self):
    user_price = self.ui.lineEdit_6.text()
    if user_price == '':
      user_price = int(0)
    else:
      user_price = int(re.sub('[^0-9]', '', self.ui.lineEdit_6.text()))
    score_window = Score_Window(self.calculate_score(user_price),self)
    score_window.show()

  def calculate_score(self,user_price):
    return abs(user_price -  self.game_instance.get_question().getPrice()) #TODO use an actual scoring algorithm


  def loginBtn(self):
    self.ui.lineEdit.text()
    self.ui.lineEdit_2.text()

  # Moves to start page
  def StartPage(self):
    self.ui.stackedWidget.setCurrentIndex(0)

  # Moves to login page
  def LoginPage(self):
    self.ui.stackedWidget.setCurrentIndex(1)

  # Moves to registration page
  def RegisterPage(self):
    self.ui.stackedWidget.setCurrentIndex(2)

  # Moves to a player's main menu  
  def PlayerMainMenu(self):
    self.stop_timer()
    self.ui.stackedWidget.setCurrentIndex(3)

  # Moves to an admin's main menu
  def AdminMainMenu(self):
    self.ui.stackedWidget.setCurrentIndex(4)

  # Moves to game page
  def GamePage(self):
    self.ui.stackedWidget.setCurrentIndex(5)
    if not self.game_instance.next_question(): #loads new questions if no new questions found
      self.game_instance.load_questions()
    self.ui.label_2.setFont(QtGui.QFont('SansSerif', 25)) #product title
    self.ui.label_3.setFont(QtGui.QFont('SansSerif', 10)) #question number
    self.load_current_question()


  
  def load_current_question(self):
    self.ui.label_3.setText(f'Q#: {self.game_instance.current_question}')
    self.ui.label_2.setText(self.game_instance.get_question().getName())
    self.ui.textBrowser.setText(self.game_instance.get_question().getDescription())
    product_pixmap = QPixmap(self.game_instance.get_question().getImagePath())
    self.ui.label_product_image.setPixmap(product_pixmap)    
    self.ui.label_product_image.setScaledContents(True)
    # self.ui.label_product_image.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored) #TODO set up changes in QT designer, i couldnt get it to work -Robert
    self.ui.textBrowser.setMinimumWidth(400)
    self.start_timer()


  # Moves to score page
  # After game is over, moves to final score page.
  def ScorePage(self):
    self.ui.stackedWidget.setCurrentIndex(6)


  def RecordsPage(self):
    self.ui.stackedWidget.setCurrentIndex(7)

  # Updates Game UI elements with data on next question
  # def next_Question():

  # Displays user's score on score page
  # def display_Score():

class Score_Window(QDialog):
  def __init__(self,score,parent=None):
    super().__init__(parent)
    self.score = score
    self.label = QLabel(str(self.score), self)
    self.label.setFont(QtGui.QFont('ComicSans', 20))
    self.setWindowTitle('Score')
    self.setGeometry(100, 100, 300, 150)
    frameGm = self.frameGeometry() #center the popup on current screen
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    self.move(frameGm.topLeft())
    
def show_error(page, error):
  # TODO - Add an error container to each page? At least login
  # error_login_label
  page.ui.error_register_label.setText(error)

# Loads images of questions for Q. Manager
# def load_Images():

app = QtWidgets.QApplication([])
w = Main_Window()
# score = Score_Window()
#window.setGeometry(0, 0, 500, 300)
w.setWindowTitle("Price Guessing Game")

w.show()
sys.exit(app.exec_())


