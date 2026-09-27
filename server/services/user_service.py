from extensions import db
from models import User, Role, UserRole

class UserService:
  
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
  def update_profile(user_id, data):
    user = User.query.filter_by(id=user_id).first()

    try:
      for key, value in data.items():
        setattr(user, key, value)
      db.session.commit()
      return user
    except ValueError as error:
      db.session.rollback()
      return str(error)
    except Exception:
      db.session.rollback()
      return "Invalid data"
    
    