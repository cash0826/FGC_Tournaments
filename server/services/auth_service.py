from extensions import db
from models import User, Role, UserRole
from utils.errors import ConflictError, ValidationError, AuthenticationError

class AuthService:
  
  @staticmethod
  def validate_password_strength(password):
    if not isinstance(password, str) or len(password) < 8:
      raise ValidationError("Password must be a string of atleast 8 characters")
    return password
  
  @staticmethod
  def create_new_user(data):
    email = data.get("email")
    raw_password = data.get("password")
    existing_email = User.query.filter_by(email=email).first()
    
    if existing_email:
      raise ConflictError("Email is already registered.")
    
    AuthService.validate_password_strength(raw_password)
    
    try:
      user = User(
        email=email,
        first_name=data.get("first_name"),
        last_name=data.get("last_name")
      )
      user.password_hash = raw_password
      db.session.add(user)
      db.session.commit()
      
    except ValueError as error:
      db.session.rollback()
      raise ValidationError(str(error)) from error
    except Exception as error:
      db.session.rollback()
      raise AppError() from error
    
  @staticmethod
  def authenticate_user(email, password):
    user = User.query.filter_by(email=email.strip().lower()).first()
    if not user or not isinstance(password, str) or not user.verify_password(password):
      raise AuthenticationError()
    return user
  
  @staticmethod
  def verify_current_password(user, current_password):
    if not isinstance(current_password, str) or not user.verify_password(current_password):
      raise AuthenticationError("Current password is incorrect.")
    return password
  
  @staticmethod
  def change_password(user, current_password, new_password):
    UserService.verify_current_password(user, current_password)
    UserService.validate_pw_strength(new_password)
    user.password_hash(new_password)
    return user