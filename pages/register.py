# =============================================================================
# register.py
# This module contains the main register functionality.
# =============================================================================

# Get Objects from 
import sys
sys.path.insert(0, '../../objects')
from user import *

# Handle a registration
def handle_register(page):
	# Get input data
	username = page.ui.lineEdit_3.text()
	password = page.ui.lineEdit_4.text()
	re_password = page.ui.lineEdit_5.text()

	# Validate
	if Player.length_check(username) or Player.length_check(password) or Player.length_check(re_password):
		clear_fields(page)
		return "Credentials have invalid length."
	elif Player.alpha_check(username) or Player.alpha_check(password):
		clear_fields(page)
		return "Only alpha numeric usernames/passwords allowed."
	elif Player.check_Username(username):
		clear_fields(page, True)
		return "Username is taken."
	else:
		Player.add_User(username, password)
		page.StartPage()

def clear_fields(page, usernameAlso=False):
	if usernameAlso: page.ui.lineEdit_3.setText("")
	page.ui.lineEdit_4.setText("")
	page.ui.lineEdit_5.setText("")