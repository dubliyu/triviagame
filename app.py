# app.py
# Main function

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from window import Ui_MainWindow
from threading import Thread
from user import *
import time
import sys
import user

# One Main Window, Multiple QStackedWidgets

class mywindow(QtWidgets.QMainWindow):
  def __init__(self):
    super(mywindow, self).__init__()
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

    self.ui.pushButton_10.clicked.connect(self.LoginPage)

    # Player Main Menu Buttons
    self.ui.pushButton_12.clicked.connect(self.GamePage)
    self.ui.pushButton_13.clicked.connect(self.RecordsPage)

    # Records Buttons
    self.ui.pushButton_18.clicked.connect(self.PlayerMainMenu)

    # Leaderboard Buttons
    self.ui.pushButton_19.clicked.connect(self.PlayerMainMenu)

    self.ui.lcdNumber.display(30)
    t = Thread(target=self._countdown)
    t.start()

  # Passover control flow login to main menu
  def passoff_login(page):
    # Get input data
    username = page.ui.lineEdit.text()
    password = page.ui.lineEdit_2.text()

    # Validate
    if Player.length_check(username) or Player.length_check(password):
      show_error(page, "Credentials have invalid length")
      page.ui.lineEdit_2.setText("")
    else:
      # Create user obj
      page.user_obj = Player(username, password)
      if page.user_obj.is_logged_in:
        page.PlayerMainMenu()
      else:
        # Bad login
        show_error(page, "Invalid Username/password combination")
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
    elif Player.check_Username(username):
      show_error(page, "Username is taken.")
      page.ui.lineEdit_3.setText("")
      page.ui.lineEdit_4.setText("")
      page.ui.lineEdit_5.setText("")
    #elif Player.is_alnum(username):
      #show_error(page, "Username can only contain alphanumeric characters.")
    else:
      # insert into user
      Player.add_User(username, password)
      page.StartPage()

  def _countdown(self):
    TIME = 30 #seconds
    for t in range(TIME, -1, -1):
      time.sleep(1)
      self.ui.lcdNumber.display(t)

  def btnClicked(self):
    self.ui.label_2.setFont(QtGui.QFont('SansSerif', 30))
    self.ui.label_2.setText("Button Clicked")

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
    self.ui.stackedWidget.setCurrentIndex(3)

  # Moves to an admin's main menu
  def AdminMainMenu(self):
    self.ui.stackedWidget.setCurrentIndex(4)

  # Moves to game page
  def GamePage(self):
    self.ui.stackedWidget.setCurrentIndex(5)

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

def show_error(page, error):
  # TODO - Add an error container to each page? At least login
  page.ui.error_register_label.setText(error)

# Loads images of questions for Q. Manager
# def load_Images():

app = QtWidgets.QApplication([])
w = mywindow()
#window.setGeometry(0, 0, 500, 300)
w.setWindowTitle("Price Guessing Game")

w.show()
sys.exit(app.exec_())


