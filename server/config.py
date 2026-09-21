import os
from datetime import timedelta

class Config:
  SECRET_KEY = os.environ.get("SECRET_KEY")
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  
  JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
  
  #access token - header only
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
  JWT_TOKEN_LOCATION = ["headers"]
  
  # refresh token - http-only cookie only
  JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
  JWT_REFRESH_COOKIE_PATH = "/api/auth"
  