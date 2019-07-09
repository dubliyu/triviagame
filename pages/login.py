# =============================================================================
# login.py
# This module contains the main login functionality.
# =============================================================================

# Get Objects from 
import sys
sys.path.insert(0, '../../objects')
from user import *

# handle login btn click
def handle_login(page):
    # Get input data
    username = page.ui.lineEdit.text()
    password = page.ui.lineEdit_2.text()

    # Validate
    if Player.length_check(username) or Player.length_check(password):
      page.ui.lineEdit_2.setText("")
      return "Credentials have invalid length."
    elif Player.alpha_check(username) or Player.alpha_check(password):
      page.ui.lineEdit_2.setText("")
      page.ui.lineEdit.setText("")
      return "Only alpha numeric usernames/passwords allowed."
    
    # Attemp to login
    page.user_obj = Player(username, password)
    if page.user_obj.is_logged_in:
        if page.user_obj.user_type == 1:
            page.AdminMainMenu()
        else:
            page.PlayerMainMenu()
    else:
        # Bad login
        page.ui.lineEdit_2.setText("")
        return "Invalid Username/password combination."