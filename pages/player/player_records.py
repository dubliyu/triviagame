# =============================================================================
# Player Submodules
# player_records.py
# This module contains the player records functionality.
# =============================================================================

# Get Objects from 
from PyQt5 import QtWidgets
import sys
sys.path.insert(0, '../../../objects')
from user import *

# Passover logic to load the records
def goto_records(page):
    # Retrieve user records
    records = page.user_obj.get_records(page.user_obj.username)

    # Create widget space
    content = QtWidgets.QWidget(page)
    layout = QtWidgets.QVBoxLayout(content)

    # Add in all records
    sumation = 0
    for record in records:
        # increment player sum
        sumation = sumation + record[1]

        # Create play time label
        play_time = str('{:.2f}'.format(record[1] / 60))
        temp_label = QtWidgets.QHBoxLayout()
        temp_label.addWidget(QtWidgets.QLabel("Played for " + play_time + " minutes", page))
      
        # Create datetime label
        temp_label.addWidget(QtWidgets.QLabel("\tAt " + str(record[3]), page))
      
        # Create Score label
        temp_label.addWidget(QtWidgets.QLabel("\tScore " + str(record[2]), page))

        # Insert temp element
        temp_label.addStretch(1)
        layout.addLayout(temp_label)
    page.ui.scrollArea.setWidget(content)

    # Set averages and total
    average_score = 0
    if len(records) > 0: average_score = sumation / len(records)
    page.ui.label_17.setText("Games Played: " + str(len(records)))
    page.ui.label_18.setText("Average Score: " + str(average_score))

    # Move to the screen
    page.ui.stackedWidget.setCurrentIndex(7)