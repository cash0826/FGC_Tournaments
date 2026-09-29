from extensions import db
from models import Role, User, UserRole
from sqlalchemy.exc import IntegrityError
from utils.errors import AppError, ConflictError, NotFoundError, ValidationError


class UserRoleService:
  
  @staticmethod
  def assign_role(user_id, role_name):
    if not isinstance(user_id, int) or user_id < 1:
      raise ValidationError("User id must be a positive integer.")
    if not isinstance(role_name, str) or not role_name.strip():
      raise ValidationError("Role is required.")

    user = User.query.filter_by(id=user_id).first()
    if not user:
      raise NotFoundError("User not found.")
    role = Role.query.filter_by(name=role_name.strip().lower()).first()
    if not role:
      raise NotFoundError("Role not found.")
    existing = UserRole.query.filter_by(user_id=user_id, role_id=role.id).first()
    if existing:
      raise ConflictError("Role already assigned to this user.")
    
    try:
      ur = UserRole(user_id=user_id, role_id=role.id)
      db.session.add(ur)
      db.session.commit()
      return ur
    except IntegrityError as error:
      db.session.rollback()
      raise ConflictError("Role already assigned to this user.") from error
    except ValueError as error:
      db.session.rollback()
      raise ValidationError(str(error)) from error
    except Exception as error:
      db.session.rollback()
      raise AppError(f"{error}", 500) from error

  @staticmethod
  def remove_role(user_id, role_name):
    if not isinstance(user_id, int) or user_id < 1:
      raise ValidationError("User id must be a positive integer.")
    if not isinstance(role_name, str) or not role_name.strip():
      raise ValidationError("Role is required.")

    user = User.query.filter_by(id=user_id).first()
    if not user:
      raise NotFoundError("User not found.")
    role = Role.query.filter_by(name=role_name.strip().lower()).first()
    if not role:
      raise NotFoundError("Role not found.")
    
    instance = UserRole.query.filter_by(user_id=user_id, role_id=role.id).first()
    
    if not instance:
      raise NotFoundError("Role is not assigned to this user.")
    
    try:
      db.session.delete(instance)
      db.session.commit()
      return instance
    except Exception as error:
      db.session.rollback()
      raise AppError(f"{error}", 500) from error
    