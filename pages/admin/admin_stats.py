# =============================================================================
# Admin Submodules
# admin_stats.py
# This module contains the admin statistics functionality.
# =============================================================================

# Get Objects from 
from PyQt5 import QtWidgets
import sys
sys.path.insert(0, '../../../objects')
from user import *

# Passover logic to load the records
def goto_stats(page):
    # Retrieve user records
    records = Player.get_statistics_records()

    # Populate the screen
    content = QtWidgets.QWidget(page)
    layout = QtWidgets.QVBoxLayout(content)
    for record in records:
      # Insert into the screen
      temp = QtWidgets.QHBoxLayout()
      temp.addWidget(QtWidgets.QLabel(str(record[0]) + "\t" , page))
      temp.addWidget(QtWidgets.QLabel("Average Score: " + '{:.2f}'.format(record[1]) + "\t" , page))
      temp.addWidget(QtWidgets.QLabel("Games Played: " + str(record[2]) + "\t" , page))

      # Add see more btn
      btn = QtWidgets.QPushButton("See More", page)
      btn.clicked.connect(lambda: page.passoff_see_more(record))

      temp.addWidget(btn)
      temp.addStretch(1)
      layout.addLayout(temp)
    page.ui.scrollArea_6.setWidget(content)

    # Move to the screen
    page.ui.stackedWidget.setCurrentIndex(12)

# Passover logic to go deeper into statistics
def goto_see_more(page, player_rec):
    # Retrieve user records
    records = Player.get_records(player_rec[0])

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
    total = 0
    if len(records) != 0: total = sumation / len(records)
    page.ui.label_17.setText("Games Played: " + str(len(records)))
    page.ui.label_18.setText("Average Score: " + '{:.2f}'.format(total))

    # Move to the screen
    page.ui.pushButton_26.clicked.connect(page.AdminMainMenu)
    page.ui.stackedWidget.setCurrentIndex(7)