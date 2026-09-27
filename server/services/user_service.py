from extensions import db
from models import User, Role, UserRole
from sqlalchemy.exc import IntegrityError
from utils.errors import AppError, ConflictError, NotFoundError, ValidationError

class UserService:
  
  @staticmethod
  def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
      raise NotFoundError("User not found.")
    return user
  
  @staticmethod
  def get_user_by_email(email):
    if not isinstance(email, str):
      raise ValidationError("Email must be a string.")
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
    if not user:
      raise NotFoundError("User not found.")
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")

    editable_fields = {
      "gamer_name", "first_name", "last_name", "bio",
      "profile_pic_url", "contact_number"
    }
    invalid_fields = data.keys() - editable_fields
    if invalid_fields:
      raise ValidationError(f"Profile fields cannot be updated: {', '.join(sorted(invalid_fields))}.")

    try:
      for key, value in data.items():
        setattr(user, key, value)
      db.session.commit()
      return user
    except ValueError as error:
      db.session.rollback()
      raise ValidationError(str(error)) from error
    except IntegrityError as error:
      db.session.rollback()
      raise ConflictError("A profile value is already in use.") from error
    except Exception as error:
      db.session.rollback()
      raise AppError("Unable to update profile.", 500) from error
    
    