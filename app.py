# app.py
# Main function

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from window import Ui_MainWindow
from threading import Thread
import time
import sys

# One Main Window, Multiple QStackedWidgets

class mywindow(QtWidgets.QMainWindow):
  def __init__(self):
    super(mywindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ui.pushButton.clicked.connect(self.LoginPage)
    self.ui.pushButton_2.clicked.connect(self.RegisterPage)

    # FIX LATER - Login button should move a user to either the player or admin main menu
    self.ui.pushButton_3.clicked.connect(self.PlayerMainMenu)

    self.ui.pushButton_4.clicked.connect(self.StartPage)
    self.ui.pushButton_7.clicked.connect(self.StartPage)

    # FIX LATER - Register button should add user to DB and return to player or admin main menu
    self.ui.pushButton_8.clicked.connect(self.StartPage)

    self.ui.pushButton_10.clicked.connect(self.LoginPage)
    self.ui.pushButton_12.clicked.connect(self.GamePage)
    #self.ui.label_2.setGeometry(QtCore.QRect(0, 0, 100, 100))

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

  # Updates Game UI elements with data on next question
  # def next_Question():

app = QtWidgets.QApplication([])
w = mywindow()
#window.setGeometry(0, 0, 500, 300)
w.setWindowTitle("Price Guessing Game")

w.show()
sys.exit(app.exec_())


