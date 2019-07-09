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
      temp.addWidget(QtWidgets.QLabel("Average Score: " + str(record[1]) + "\t" , page))
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