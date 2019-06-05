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
from enum import Enum

# User type enum
class user_type(Enum):
  STANDARD = 0
  PRO = 1
  ADMIN = 2

class Player:
  num_users = 0

  def __init__(self, username, pw):
    self.username = username
    self.password = pw
    #self.user = user_type
    games_played = 0

# Checks that password inputs match
def password_Check(pw, repw):
  if pw == repw:
    return True
  else:
    return False

# Validates length of username between 2 to 20 characters
def username_Length(username):
  MIN_LENGTH = 2
  MAX_LENGTH = 20
  if len(username) < MIN_LENGTH:
    print('Username too short.')
  if len(username) > MAX_LENGTH:
    print('Username too long.')

# Validates length of password between 6 to 20 characters
def password_Length(password):
  MIN_LENGTH = 6
  MAX_LENGTH = 20
  if len(password) < MIN_LENGTH:
    print('Password too short.')
  if len(password) > MAX_LENGTH:
    print('Password too long.')

# Upgrades player to pro
#def upgrade_Pro()

# Adds user to database
def add_User(username, password):
  # Get a hashed password
  hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

  # Store the user
  connection = sqlite3.connect('app.db')
  c = connection.cursor()
  c.execute("insert into users (username, hash) values (?, ?)", (username, hashed))
  connection.commit()
  connection.close()

# Checks that an user has a valid password
def authorize_Login(username, password):
  connection = sqlite3.connect('app.db')
  c = connection.cursor()
  c.execute("select * from users where username=?", username)
  connection.close()
  for row in c:
    # Check matching row
    if bcrypt.checkpw(password.encode('utf-8'), row[1]):
      return True
    else:
      return False

  # There was no match
  return False

# Checks existing usernames 
def check_Username(username):
  connection = sqlite3.connect('app.db')
  c.execute("select username from users where username=?", username)
  connection.close()
  for row in c:
    # There was a matching row i.e. username allready exists
    return False
  # There was no match
  return True

username = input('Username: ')
username_Length(username)

password = input('Password: ')
password_Length(password)
re_password = input('Re-enter Password: ')
#player1 = Player(username, password, STANDARD)

print(password_Check(password, re_password))

