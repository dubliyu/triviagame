# app.py
# Main function

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from window import Ui_MainWindow
import sys

# One Main Window, Multiple QStackedWidgets

class mywindow(QtWidgets.QMainWindow):
  def __init__(self):
    super(mywindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.pushButton.clicked.connect(self.btnClicked)
    self.ui.label.setGeometry(QtCore.QRect(0, 0, 100, 100))
  def btnClicked(self):
    self.ui.label.setFont(QtGui.QFont('SansSerif', 30))
    self.ui.label.setText("Button Clicked")

app = QtWidgets.QApplication([])
w = mywindow()
#window.setGeometry(0, 0, 500, 300)
w.setWindowTitle("Price Guessing Game")

w.show()
sys.exit(app.exec_())


