from extensions import db
from .user_service import find_user_by_email

def validate_pw_strength(password):
  if not isinstance(password, str) or len(password) < 8:
    raise ValueError("Password must be at least 8 characters")


def authenticate_user(email, password):
  user = UserService.get_user_by_email(email=email)
  if not user or not isinstance(password, str) or not user.verify_password(password):
    raise ValueError("Invalid email or password")
  return user
