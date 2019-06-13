# user.py
# User classes and methods
#
# User Classes:
# 1. Standard Player
# 2. Pro Player
# 3. Admin

import sys
import sqlite3
import bcrypt
import re
from enum import Enum

# Statics
MIN_LENGTH = 4
MAX_LENGTH = 20

# User type enum
class user_type(Enum):
  STANDARD = 0
  PRO = 1
  ADMIN = 2

# User class
class Player:
  # Class properties
  user_id = -1
  games_played = -1
  is_logged_in = False
  username = ""
  user_type = -1

  def __init__(self, username, password):
    # Attempt to retrieve user from db
    db_data = self.attemp_login(username, password)

    # Check if user was logged in
    if not db_data == []:
      # Set instance properties
      self.is_logged_in = True
      self.user_id = db_data[0]
      self.username = db_data[1]
      self.games_played = db_data[3]
      self.user_type = db_data[4]

  # Checks that password inputs match
  @staticmethod
  def password_Check(pw, repw):
    return pw == repw

  # Validates length of username/password
  @staticmethod
  def length_check(word):
    return len(word) < MIN_LENGTH or len(word) > MAX_LENGTH

  # Validate alpha numeric
  def alpha_check(word):
    return not re.match('^\w+$', word)

  # Checks input against existing usernames 
  @staticmethod
  def check_Username(username):
    connection = sqlite3.connect('app.db')
    c = connection.cursor()
    c.execute("select username from users where username=?", (username,))
    fetch = c.fetchone()
    connection.close()
    return not fetch == None

  # Adds user to database
  @staticmethod
  def add_User(username, password):
    # Get a hashed password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Store the user
    connection = sqlite3.connect('app.db')
    connection.execute("insert into users (username, hash) values (?, ?);", (username, hashed))
    connection.commit()
    connection.close()

  # Upgrades player to pro
  def upgrade_Pro(self):
    connection = sqlite3.connect('app.db')
    connection.execute("update users set user_type=? where user_id=?;", (user_type.PRO, self.user_id))
    connection.commit()
    connection.close()

  # Attempt a login
  def attemp_login(self, username, password):
    # Get user from db
    connection = sqlite3.connect('app.db')
    c = connection.cursor()
    c.execute("select rowid, * from users where username=?;", (username,))
    fetch = c.fetchone()
    connection.close()

    # Check match
    if fetch == None:
      return []

    # Check password
    if bcrypt.checkpw(password.encode('utf-8'), fetch[2]):
      return fetch

    # Bad password
    return []
