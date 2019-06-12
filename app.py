# app.py
# Main function

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from window import Ui_MainWindow
from threading import Thread
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
    # FIX LATER - Login button (pushButton_3) should move a user to either the player or admin main menu
    self.ui.pushButton_3.clicked.connect(self.PlayerMainMenu)
    self.ui.pushButton_4.clicked.connect(self.StartPage)
    
    # Register Page Buttons
    # FIX LATER - Register button (pushbutton_8) should add user to DB and return to player or admin main menu
    self.ui.pushButton_8.clicked.connect(self.Register)
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

  def username_Msg(self):
    self.ui.label_14.setText('Username must only contain alphanumeric characters and be 2 to 20 characters long.')

  def password_Match_Msg(self):
    self.ui.label_15.setText("Passwords must match.")

  def Register(self):
    username = self.ui.lineEdit_3.text()
    password = self.ui.lineEdit_4.text()
    re_password = self.ui.lineEdit_5.text()

    if user.validate_Username(username) == False:
      self.username_Msg()
      return
    if user.username_Length(username) != 'VALID':
      self.username_Msg()
      return

    print('Registration successful!')

    #password_Match_Msg if not validate_Password(password)

    

# Loads images of questions for Q. Manager
# def load_Images():

app = QtWidgets.QApplication([])
w = mywindow()
#window.setGeometry(0, 0, 500, 300)
w.setWindowTitle("Price Guessing Game")

w.show()
sys.exit(app.exec_())


