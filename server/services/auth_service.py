from extensions import db
from models import User
from sqlalchemy.exc import IntegrityError
from utils.errors import AppError, AuthenticationError, ConflictError, ValidationError

class AuthService:
  
  @staticmethod
  def validate_password_strength(password):
    if not isinstance(password, str) or len(password) < 8:
      raise ValidationError("Password must be a string of at least 8 characters.")
  
  @staticmethod
  def create_new_user(data):
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")

    email = data.get("email")
    raw_password = data.get("password")
    if not isinstance(email, str) or not email.strip():
      raise ValidationError("Email is required.")

    email = email.strip().lower()
    existing_email = User.query.filter_by(email=email).first()
    
    if existing_email:
      raise ConflictError("Email is already registered.")
    
    AuthService.validate_password_strength(raw_password)
    
    try:
      user = User(email=email)
      for field in ("first_name", "last_name"):
        if field in data:
          setattr(user, field, data[field])
      user.password_hash = raw_password
      db.session.add(user)
      db.session.commit()
    except ValueError as error:
      db.session.rollback()
      raise ValidationError(str(error)) from error
    except IntegrityError as error:
      db.session.rollback()
      raise ConflictError("Email is already registered.") from error
    except Exception as error:
      db.session.rollback()
      raise AppError(f"{error}", 500) from error

    return user

  @staticmethod
  def authenticate_user(email, password):
    if not isinstance(email, str) or not email.strip() or not password:
      raise ValidationError("Email and password are required.")
    user = User.query.filter_by(email=email.strip().lower()).first()
    if not user or not isinstance(password, str) or not user.verify_password(password):
      raise AuthenticationError()
    return user
  
  @staticmethod
  def verify_current_password(user, current_password):
    if (not isinstance(current_password, str)
        or not user.verify_password(current_password)):
      raise AuthenticationError("Current password is incorrect.")
  
  @staticmethod
  def change_password(user, current_password, new_password):
    AuthService.verify_current_password(user, current_password)
    AuthService.validate_password_strength(new_password)
    try:
      user.password_hash = new_password
      db.session.commit()
    except ValueError as error:
      db.session.rollback()
      raise ValidationError(str(error)) from error
    except Exception as error:
      db.session.rollback()
      raise AppError(f"{error}", 500) from error
    return user
  
  @staticmethod
  def delete_profile(user, current_password):   # For user to delete their own profile
    AuthService.verify_current_password(user, current_password)
    
    try:
      db.session.delete(user)
      db.session.commit()
    except Exception as error:
      db.session.rollback()
      
      raise AppError(f"{error}", 500) from error
    
    