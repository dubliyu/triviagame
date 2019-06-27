# =============================================================================
# app.py
# This module contains the main function and GUI functionality.
# =============================================================================
#
# Note: To launch game, 'python app.py'.
# Note 2: To update .ui file, compile the .ui file to a .py file with
#         'pyuic5 window.ui -o window.py'.
#

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from window import Ui_MainWindow
from threading import Thread, currentThread
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
  time_left = 0

  def __init__(self):
    super(Main_Window, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.setStyleSheet(open('style.css').read())

    # Load Logo
    logo_pixmap = QtGui.QPixmap('logo.png')
    self.ui.label_logo.setPixmap(logo_pixmap.scaled(1000, 1000, QtCore.Qt.KeepAspectRatio)) 
    self.ui.stackedWidget.setCurrentIndex(0)
  
    # Start Page Elements
    self.ui.pushButton.clicked.connect(self.LoginPage)
    self.ui.pushButton_2.clicked.connect(self.RegisterPage)

    # Login Page Elements
    self.ui.pushButton_3.clicked.connect(self.passoff_login)
    self.ui.lineEdit_2.returnPressed.connect(self.ui.pushButton_3.click)
    self.ui.pushButton_4.clicked.connect(self.StartPage)
    self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
    
    # Register Page Elements
    self.ui.pushButton_8.clicked.connect(self.passoff_register)
    self.ui.pushButton_7.clicked.connect(self.StartPage)
    self.ui.lineEdit_5.returnPressed.connect(self.ui.pushButton_8.click)
    self.ui.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
    self.ui.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Password)

    self.ui.pushButton_10.clicked.connect(self.PlayerMainMenu)

    # Player Main Menu Elements
    self.ui.pushButton_12.clicked.connect(self.GamePage)
    self.ui.pushButton_13.clicked.connect(self.passoff_records)
    self.ui.pushButton_14.clicked.connect(self.passoff_leader)
    self.ui.pushButton_15.clicked.connect(self.QuestionManagerPage)
    #self.ui.pushButton_16.clicked.connect(self.QuitBtn)

    # Game Interface Elements
    self.ui.pushButton_9.clicked.connect(self.next_question_button)
    self.ui.lineEdit_6.returnPressed.connect(self.ui.pushButton_9.click)
    self.ui.lcdNumber.display(30)

    # Score Page Elements
    self.ui.pushButton_17.clicked.connect(self.PlayerMainMenu)

    # Records Buttons
    self.ui.pushButton_18.clicked.connect(self.PlayerMainMenu)

    # Leaderboard Elements
    self.ui.pushButton_19.clicked.connect(self.PlayerMainMenu)

    # Question Manager Elements
    self.ui.pushButton_20.clicked.connect(self.PlayerMainMenu)

    # Add Question Menu Elements
    self.ui.pushButton_22.clicked.connect(self.PlayerMainMenu)
    self.ui.open_image_button.clicked.connect(self.add_image)

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

  # Passover logic to load the records
  def passoff_records(page):
    # Retrieve user records
    records = page.user_obj.get_records()

    # Populate the screen
    content = QtWidgets.QWidget(page)
    layout = QtWidgets.QVBoxLayout(content)
    sumation = 0
    for record in records:
      # Insert into the screen
      sumation = sumation + record[1]
      temp = QtWidgets.QHBoxLayout()
      temp.addWidget(QtWidgets.QLabel("Played for " + str('{:.2f}'.format(record[1] / 60)) + " minutes", page))
      temp.addWidget(QtWidgets.QLabel("At " + str(record[3]), page))
      temp.addWidget(QtWidgets.QLabel("Score " + str(record[2]), page))
      temp.addStretch(1)
      layout.addLayout(temp)
    page.ui.scrollArea.setWidget(content)

    # Set aveages and total
    page.ui.label_17.setText("Games Played: " + str(len(records)))
    page.ui.label_18.setText("Average Score: " + str(sumation / len(records)))

    # Move to the screen
    page.ui.stackedWidget.setCurrentIndex(7)


  def passoff_leader(page):
    # Retrieve user records
    records = Player.get_top_five()

    # Populate the screen
    content = QtWidgets.QWidget(page)
    layout = QtWidgets.QVBoxLayout(content)
    count = 1
    for record in records:
      # Insert into the screen
      temp = QtWidgets.QHBoxLayout()
      temp.addWidget(QtWidgets.QLabel("# " + str(count) + "\t" , page))
      temp.addWidget(QtWidgets.QLabel(str(record[1]) + "\t" + str(record[2]), page))
      temp.addStretch(1)
      layout.addLayout(temp)
      count = count + 1
    page.ui.scrollArea_2.setWidget(content)

    # Move to the screen
    page.ui.stackedWidget.setCurrentIndex(8)

  def start_timer(self):
    self.timer_thread = Thread(target = self._countdown)
    self.timer_thread.daemon= True
    self.timer_thread.running = True
    self.timer_thread.start()

  def _countdown(self):
    TIME = 30 #seconds
    count = TIME
    running_thread = currentThread()
    while getattr(running_thread, "running", True) and count >= 0:
      self.ui.lcdNumber.display(count)
      self.time_left = count
      time.sleep(1)
      count = count - 1
      if count == 0:
        self.ui.lineEdit_6.setText('0')
        self.ui.lineEdit_6.setReadOnly(True)
        
  def stop_timer(self): 
    self.timer_thread.running = False
    self.timer_thread.join()

  def next_question_button(self):
    if self.next_question_pushed == False: #if pushing submit button for first time
      if self.display_score(): #if price is correctly formatted
        self.next_question_pushed = True
        self.ui.lineEdit_6.setReadOnly(True)
        self.ui.pushButton_9.setText('NEXT')
        self.stop_timer()
      else:
        QtWidgets.QMessageBox.about(self, 'Error','Invalid price formatting.')
    else:
      self.ui.lineEdit_6.setReadOnly(False)
      self.ui.lineEdit_6.setText('')
      self.ui.pushButton_9.setText('SUBMIT')
      if self.game_instance.next_question() is False: #if the last question has been reached, show score page
        self.next_question_pushed = False
        self.ScorePage()
      else:
        self.load_current_question()
        self.next_question_pushed = False

  def display_score(self):
    user_price = str(self.ui.lineEdit_6.text())
    price_int = 0
    if re.match('^[+-]?[0-9]{1,3}(?:(,[0-9]{3})*|([0-9]{3})*)(?:\.[0-9]{2})?$', user_price ): #regex for price formatting
      if not '.' in user_price:
        price_int = int(re.sub('[^0-9]', '', user_price)) * 100 #if no cents indicated, make sure correct int format
      else:
        price_int = int(re.sub('[^0-9]', '', user_price)) #if cents used
    else:
      return False
    current_score = self.game_instance.calculate_score(price_int, 30 - self.time_left)
    score_window = Score_Window(current_score.get_score(), current_score.get_label(), self)
    score_window.show()
    return True

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
    self.ui.pushButton_9.setText('SUBMIT')
    if not self.game_instance.next_question(): #loads new questions if no new questions found
      self.game_instance.load_questions()
    self.ui.label_2.setFont(QtGui.QFont('SansSerif', 25)) #product title
    self.ui.label_3.setFont(QtGui.QFont('SansSerif', 10)) #question number
    self.load_current_question()
    self.start_time = time.time()

  def LeaderboardPage(self):
    self.ui.stackedWidget.setCurrentIndex(9)

  # Moves to question manager
  def QuestionManagerPage(self):
    self.ui.stackedWidget.setCurrentIndex(10)

  # Moves to add question menu
  def AddQuestionPage(self):
    self.ui.stackedWidget.setCurrentIndex(11)
  
  def load_current_question(self):
    self.ui.label_3.setText(f'Q#: {self.game_instance.current_question}')
    self.ui.label_2.setText(self.game_instance.get_question().getName())
    self.ui.textBrowser.setText(self.game_instance.get_question().getDescription())
    product_pixmap = QtGui.QPixmap(self.game_instance.get_question().getImagePath())
    self.ui.label_product_image.setPixmap(product_pixmap)    
    self.ui.label_product_image.setScaledContents(True)
    # self.ui.label_product_image.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored) #TODO set up changes in QT designer, i couldnt get it to work -Robert
    self.ui.textBrowser.setMinimumWidth(400)
    self.start_timer()

  # Moves to score page
  # After game is over, moves to final score page.
  def ScorePage(self):
    self.ui.stackedWidget.setCurrentIndex(6)
    self.game_instance.write_game(self.user_obj.username, self.start_time) #writes game log to DB
    self.ui.label_11.setText(str(self.game_instance.get_final_score()))

  # Opens image from file dialog
  def add_image(self):
    file_dialog = QtWidgets.QFileDialog(self)
    file_dialog.setNameFilters(['Images (*.png *.jpg)'])
    file_dialog.selectNameFilter('Images (*.png *.jpg)')
    #file_dialog.setFileMode(QFileDialog.ExistingFile)
    path = file_dialog.getOpenFileName(self, 'Add Image')
    print(path)
    # file = open(name, 'r')


  #def QuitBtn(self):
    #sys.exit(app.exec_())

  # Displays user's score on score page
  # def display_Score():

class Score_Window(QtWidgets.QDialog):
  def __init__(self,score,title,parent=None):
    super().__init__(parent)
    self.score = score
    self.label = QtWidgets.QLabel(str(self.score), self)
    self.label.setFont(QtGui.QFont('ComicSans', 20))
    self.setWindowTitle(title)
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

