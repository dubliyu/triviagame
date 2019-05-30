import sys
from PyQt5 import QtGui, 

# One Main Window, Multiple QStackedWidgets

app = QtGui.QApplication([])

window = QtGui.QWidget()
window.setGeometry(0, 0, 500, 300)
window.setWindowTitle("Price Guessing Game")

window.show()


