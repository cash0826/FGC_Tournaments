from extensions import db
from models import User, Role, UserRole

class UserService:
  
  @staticmethod
  def signup_user(data):
    # TODO: create_user
    pass
  
  @staticmethod
  def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()
  
  @staticmethod
  def get_user_by_email(email):
    return User.query.filter_by(email=email.strip().lower()).first()
  
  @staticmethod
  def get_all_users():
    return User.query.all()
  
  @staticmethod
  def get_roles_for_user(user_id):
    roles = (
      db.session.query(Role.name)
      .join(UserRole, UserRole.role_id == Role.id)
      .filter(UserRole.user_id == user_id)
      .all()
    )
    return [r[0] for r in roles]

  @staticmethod
  def authenticate_user(email, password):
    user = UserService.get_user_by_email(email=email)
    if not user or not isinstance(password, str) or not user.verify_password(password):
      raise ValueError("Invalid email or password")
    return user
  
  @staticmethod
  def verify_current_password(user, current_password):
    if not isinstance(current_password, str) or not user.verify_password(current_password):
      raise ValueError("current_password_is_incorrect")
    
  @staticmethod
  def validate_pw_strength(password):
    if not isinstance(password, str) or len(password) < 8:
      raise ValueError("Password must be at least 8 characters")
  
  @staticmethod
  def change_password(user, current_password, new_password):
    UserService.verify_current_password(user, current_password)
    UserService.validate_pw_strength(new_password)
    user.password_hash(new_password)
    return user
  