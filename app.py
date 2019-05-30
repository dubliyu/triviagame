import sys
from PyQt5 import QtGui, QtWidgets

# One Main Window, Multiple QStackedWidgets

app = QtWidgets.QApplication([])
window = QtWidgets.QWidget()
window.setGeometry(0, 0, 500, 300)
#window.setWindowTitle("Price Guessing Game")

window.show()
sys.exit(app.exec_())

