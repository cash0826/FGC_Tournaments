# File created for reference only. PW methods created in User data model

import bcrypt

def hash_password(password):
  salt = bcrypt.gensalt()
  return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')    # decode converts it back from binary

def verify(password, hashed_password):
  return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))