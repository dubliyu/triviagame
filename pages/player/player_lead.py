# =============================================================================
# Player Submodules
# player_lead.py
# This module contains the player leaderboards functionality.
# =============================================================================

# Get Objects from 
from PyQt5 import QtWidgets
import sys
sys.path.insert(0, '../../../objects')
from user import *

# Passover logic to load the records
def goto_leaderboards(page):
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
      temp.addWidget(QtWidgets.QLabel(str(record[0]) + "\t" + str(record[2]), page))
      temp.addStretch(1)
      layout.addLayout(temp)
      count = count + 1
    page.ui.scrollArea_2.setWidget(content)
    page.ui.scrollArea_2.setStyleSheet("background-color: #303030")

    # Move to the screen
    page.ui.stackedWidget.setCurrentIndex(8)