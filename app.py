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
from PIL import Image
from scraper import *
from question import *
from widgets import *
import re
import time
import sys
from game import Game

# Get Objects from subdirs
sys.path.insert(0, './objects')
from user import *

# Get shared pages from subdirs
sys.path.insert(0, './pages')
import login as login_page
import register as register_page

# Get player pages from subdirs
sys.path.insert(0, './pages/player')
import player_records
import player_lead

# Get admin pages from subdirs
sys.path.insert(0, './pages/admin')
import admin_stats


# One Main Window, Multiple QStackedWidgets
class Main_Window(QtWidgets.QMainWindow):
  #Variables
  next_question_pushed = False
  game_instance = Game()
  grid_row = 0
  grid_column = 0
  timer_thread  = Thread()
  timer_thread.start()
  time_left = 0
  current_image_selection = Path('img\default.jpeg')
  question_manager_widget = None
  edit_question = None

  def __init__(self):
    super(Main_Window, self).__init__()
    frameGm = self.frameGeometry() # Center the windows on the current screen 
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    grid_radio_buttons = QtWidgets.QButtonGroup()
    self.question_manager_widget = QuestionManagerWidget() #start instance

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.setStyleSheet(open('style.css').read())
    self.ui.stackedWidget.setCurrentIndex(0)
    self.showMaximized()

    # Load Logo
    logo_pixmap = QtGui.QPixmap('logo.png')
    self.ui.label_logo.setPixmap(logo_pixmap.scaled(1000, 900, QtCore.Qt.KeepAspectRatio))
    self.ui.label_19.setPixmap(logo_pixmap.scaled(700, 500, QtCore.Qt.KeepAspectRatio))
    self.ui.label.setPixmap(logo_pixmap.scaled(700, 500, QtCore.Qt.KeepAspectRatio)) 

    # ======================================================================= #
    #                                  Buttons                                #
    # ======================================================================= #

    # Start Page Elements
    self.ui.pushButton.clicked.connect(self.LoginPage)
    self.ui.pushButton_2.clicked.connect(self.RegisterPage)
    self.ui.pushButton_28.clicked.connect(self.quitBtn)

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

    # Admin Main Memnu elements
    self.ui.pushButton_5.clicked.connect(self.QuestionManagerPage)
    self.ui.pushButton_6.clicked.connect(self.passoff_stats)
    self.ui.pushButton_11.clicked.connect(self.quitBtn)

    # Player Main Menu Elements
    self.ui.pushButton_12.clicked.connect(self.GamePage)
    self.ui.pushButton_13.clicked.connect(self.passoff_records)
    self.ui.pushButton_14.clicked.connect(self.passoff_leaderboards)
    self.ui.pushButton_15.clicked.connect(self.QuestionManagerPage)
    self.ui.pushButton_16.clicked.connect(self.quitBtn)

    # Game Interface Elements
    self.ui.pushButton_10.clicked.connect(self.quitGame)
    self.ui.pushButton_9.clicked.connect(self.next_question_button)
    self.ui.lineEdit_6.returnPressed.connect(self.ui.pushButton_9.click)
    self.ui.lcdNumber.display(30)

    # Score Page Elements
    self.ui.pushButton_17.clicked.connect(self.PlayerMainMenu)

    # Records Buttons
    self.ui.pushButton_18.clicked.connect(self.return_menu_records)

    # Leaderboard Elements
    self.ui.pushButton_19.clicked.connect(self.PlayerMainMenu)

    # Question Manager Buttons
    self.ui.pushButton_20.clicked.connect(self.return_menu_question)
    self.ui.pushButton_21.clicked.connect(self.AddQuestionPage)
    
    # Add a Question Menu Elements
    self.ui.pushButton_22.clicked.connect(self.cancelQuestion)
    self.ui.lineEdit_8.setMaxLength(80)
    self.grid_radio_buttons = QtWidgets.QButtonGroup()
    self.ui.pushButton_23.clicked.connect(self.scrape_from_url)
    self.ui.pushButton_25.clicked.connect(lambda: self.add_question_from_manager())
    self.ui.open_image_button.clicked.connect(self.add_image)
    self.ui.lcdNumber.display(30)

    # User Statistics Elements
    self.ui.pushButton_27.clicked.connect(self.AdminMainMenu)

  def return_menu_records(self):
    if self.user_obj.user_type == 1: # If admin
      self.passoff_stats()
    else:
      self.PlayerMainMenu()

  def return_menu_question(self):
    if self.user_obj.user_type == 1:
      self.AdminMainMenu()
    else:
      self.PlayerMainMenu()

  # Passover control flow login to main menu
  def passoff_login(page):
    error = login_page.handle_login(page)
    if error != None: show_error(page, error)

  # Passover control flow from register to login
  def passoff_register(page):
    error = register_page.handle_register(page)
    if error != None: show_error(page, error)

  # Passover control from player menu to records
  def passoff_records(page):
    player_records.goto_records(page)

  # Passover control from player menu to records
  def passoff_leaderboards(page):
    player_lead.goto_leaderboards(page)

  # Passover control from admin menu to statistics
  def passoff_stats(page):
    admin_stats.goto_stats(page)

  # Passover control from admin statistics to players individual statistics
  def passoff_see_more(page, records):
    admin_stats.goto_see_more(page, records)

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
        #QtWidgets.QMessageBox.about(self, 'Error','Invalid price formatting.')
        show_error(self, 'Invalid price formatting.')
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

    msg = 'Your guess is ' + current_score.get_label() + '!\n\n Your score is ' + str(current_score.get_score()) + ' points!'
    score_prompt = QtWidgets.QMessageBox.information(self, 'Score', msg, QtWidgets.QMessageBox.Ok)
    if score_prompt == QtWidgets.QMessageBox.Ok:
      pass

    # score_window = Score_Window(current_score.get_score(), current_score.get_label(), self)
    # score_window.setStyleSheet("background-color: #212121")
    # score_window.show()
    return True

  def loginBtn(self):
    self.ui.lineEdit.text()
    self.ui.lineEdit_2.text()

  def quitBtn(self):
    self.close()

  # ========================================================================= #
  #                         Page Navigation Functions                         #
  # ========================================================================= #

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
    self.current_image_selection = Path('img\default.jpeg')
    self.ui.stackedWidget.setCurrentIndex(9)
    self._reset_question_manager()

  # Moves to add question menu
  def AddQuestionPage(self):
    self.ui.stackedWidget.setCurrentIndex(10)

  # Exits current game and moves to Player Menu from Game interface
  def quitGame(self):
    quit_prompt = QtWidgets.QMessageBox.question(self, 'Quit Game', 'Current score will be discarded', QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    if quit_prompt == QtWidgets.QMessageBox.Ok:
      self.PlayerMainMenu()
    if quit_prompt == QtWidgets.QMessageBox.Cancel:
      pass

  def load_current_question(self):
    self.ui.label_3.setText(f'Q#: {self.game_instance.current_question}')
    self.ui.label_2.setText(self.game_instance.get_question().getName())
    self.ui.textBrowser.setText(self.game_instance.get_question().getDescription())
    product_pixmap = QtGui.QPixmap(self.game_instance.get_question().getImagePath())
    self.ui.label_product_image.setPixmap(product_pixmap.scaled(self.ui.label_product_image.size(), QtCore.Qt.KeepAspectRatio))    
    self.ui.textBrowser.setMinimumWidth(400)
    self.start_timer()

  # Moves to score page
  # After game is over, moves to final score page.
  def ScorePage(self):
    self.ui.stackedWidget.setCurrentIndex(6)
    self.game_instance.write_game(self.user_obj.username, self.start_time) #writes game log to DB
    self.ui.label_11.setText(str(self.game_instance.get_final_score()))

  def scrape_from_url(self):
    # print ('Attempting scrape')
    url = self.ui.lineEdit_7.text()
    if is_Amazon_URL(url) == False:
      show_error(self, 'Invalid URL')
      return
    soup = open_url(url)
    title = scrape_title(soup)
    self.grid_column = 0
    self.grid_row = 0
    self.ui.lineEdit_8.setText(title)
    self.ui.lineEdit_9.setText(str(scrape_price(soup)))
    self.ui.plainTextEdit.setPlainText(str(scrape_desc(soup)))
    scraped_images = scrape_Image_URLs(soup)
    # print(scraped_images)
    imagepaths = download_images(title[:8], scraped_images)
    
    for path in imagepaths:
      self.add_image_to_grid(path)

  #adds an image to currently free grid space, using a Path to the image
  def add_image_to_grid(self, path, checked=False):
    image = QtGui.QPixmap(os.fspath(path))
    image_box = QtWidgets.QVBoxLayout()
    image_label = QtWidgets.QLabel()
    image_label.setPixmap(image.scaled(image_label.size()/2, QtCore.Qt.KeepAspectRatio))
    # image_label.setScaledContents(True)
    image_box.addWidget(image_label)
    radio_button = QtWidgets.QRadioButton()
    radio_button.toggled.connect(lambda: self.set_current_img(path))
    self.grid_radio_buttons.addButton(radio_button) 
    image_box.addWidget(radio_button, 0, QtCore.Qt.AlignCenter)
    self.ui.gridLayout_3.addLayout(image_box, self.grid_row , self.grid_column)

    if checked:
      radio_button.setChecked(True)

    if self.grid_column is 0:
      if self.grid_row == 0:
        radio_button.setChecked(True)
      self.grid_column = 1
    else:
      self.grid_column = 0
      self.grid_row += 1

  # Opens image from file dialog
  def add_question_from_manager(self):
    name = str(self.ui.lineEdit_8.text())
    user_price = str(self.ui.lineEdit_9.text())
    description = str(self.ui.plainTextEdit.toPlainText())
    price = 0
    if re.match('^[+-]?[0-9]{1,3}(?:(,[0-9]{3})*|([0-9]{3})*)(?:\.[0-9]{2})?$', user_price ): #regex for price formatting
      if not '.' in user_price:
        price = int(re.sub('[^0-9]', '', user_price)) * 100 #if no cents indicated, make sure correct int format
      else:
        price = int(re.sub('[^0-9]', '', user_price)) #if cents used
    else:
      return False

    path = self.current_image_selection
    question = Question(name, price, description)
    if question:
      new_path = question.img_path #not using getter because it returns default if the file is not currently there
      im = Image.open(path)
      im = im.convert('RGB')
      im.save(new_path, 'JPEG') #converts to jpeg for compression
      if os.path.isdir("./temp"):
        for file in Path('temp').iterdir():
          os.remove(file)
    if self.edit_question:
      self.edit_question.setName(name)
      print(f'New name: {self.edit_question.getName()}')
      self.edit_question.setPrice(user_price)
      self.edit_question.setDescription(user_price)
      new_path = self.edit_question.generateImagePath()
      self.edit_question.updateQuestion()
    else:
      print('whoops its saving a new question')
      question = Question(name, price, description)
      new_path = question.img_path
      self.question_manager_widget.add_question_widget(question)

    im = Image.open(path)
    im = im.convert('RGB')
    im.save(new_path, 'JPEG') #converts to jpeg for compression
    # shutil.copy(str(path), new_path)
    for file in Path('temp').iterdir():
      os.remove(file)

    self.ui.lineEdit_8.setText('')
    self.ui.lineEdit_9.setText('')
    self.ui.plainTextEdit.setPlainText('')
    self.ui.lineEdit_7.setText('')
    self.grid_column = 0
    self.grid_row = 0
    self.clear_grid()
    self.current_image_selection = Path('img\default.jpeg')
    self.edit_question = None
    self.QuestionManagerPage()

  def clear_grid(self):
    while self.ui.gridLayout_3.count():
      parent = self.ui.gridLayout_3.takeAt(0)
      while parent.count():
        child = parent.takeAt(0)
        if child.widget():
          child.widget().deleteLater()

  def populate_question_manager(self):
    self.ui.scrollArea_3.setAutoFillBackground(False)
    self.question_manager_widget = QuestionManagerWidget()
    for qid in Question.get_question_ids():
      self._add_question_to_manager(Question.createQuestion(qid))

    # self.ui.scrollArea_3.setFixedHeight(self.question_manager_widget.height())
    self.ui.scrollArea_3.setWidget(self.question_manager_widget)
    self.ui.scrollArea_3.setAutoFillBackground(False)
    pal = QPalette()
    pal.setColor(QtGui.QPalette.Background, QtCore.Qt.darkGray)
    self.ui.scrollArea_3.setPalette(pal) #TODO this isnt working

  def _add_question_to_manager(self, question):
    buttons = self.question_manager_widget.add_question_widget(question)
    buttons[0].clicked.connect(lambda: self._open_question_edit(question))
    buttons[1].clicked.connect(lambda: self.deleteQuestion(question))

  def _delete_question_from_manager(self, question):
    Question.removeQuestion(question.getID())
    self._reset_question_manager()
    return

  def _open_question_edit(self, question):
    self.ui.lineEdit_7.setText('')
    self.ui.lineEdit_8.setText(question.getName())
    self.ui.lineEdit_9.setText(f'{(question.getPrice()/100):.2f}')
    self.ui.plainTextEdit.setPlainText(question.getDescription())
    self.add_image_to_grid(question.getImagePath(), True)
    self.edit_question = question
    self.AddQuestionPage()
    return

  def _reset_question_manager(self):
    self.question_manager_widget.deleteLater()
    self.populate_question_manager()

  # Empties Add Question menu fields and moves to Question Manager page
  def cancelQuestion(self):
    back_prompt = QtWidgets.QMessageBox.question(self, 'Go Back', 'Current data will be discarded', QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    if back_prompt == QtWidgets.QMessageBox.Ok:
      self.QuestionManagerPage()
      self.ui.lineEdit_7.setText('')
      self.ui.lineEdit_8.setText('')
      self.ui.lineEdit_9.setText('')
      self.ui.plainTextEdit.setPlainText('')
      self.clear_grid()
      self.edit_question = None
    if back_prompt == QtWidgets.QMessageBox.Cancel:
      pass

  def deleteQuestion(self, question):
    back_prompt = QtWidgets.QMessageBox.question(self, 'Delete', 'Question will be permanently erased',QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    if back_prompt == QtWidgets.QMessageBox.Ok:
      self._delete_question_from_manager(question)
    if back_prompt == QtWidgets.QMessageBox.Cancel:
      pass

  def set_current_img(self, path):
    self.current_image_selection = path

  def add_image(self):
    file_dialog = QtWidgets.QFileDialog(self)
    file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
    path = file_dialog.getOpenFileName(self, 'Add Image', '', "Images (*.jpg, *.png)")[0]
    self.add_image_to_grid(path, True)

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
    
# Shows dialog prompt QMessageBox to user with passed error.
def show_error(page, error):
  error_msg = error
  error_prompt = QtWidgets.QMessageBox.warning(page, 'Error', error_msg, QtWidgets.QMessageBox.Ok)
  if error_prompt == QtWidgets.QMessageBox.Ok:
    pass

if __name__ == '__main__':
  app = QtWidgets.QApplication([])
  w = Main_Window()
  # score = Score_Window()
  #window.setGeometry(0, 0, 500, 300)
  w.setWindowTitle("Price Guessing Game")

  w.show()
  sys.exit(app.exec_())
  delete_Folder(temp)



