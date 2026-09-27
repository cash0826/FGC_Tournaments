from extensions import db
from models import Role, UserRole

class UserRoleService:
  
  @staticmethod
  def assign_role(user_id, role_name):
    role = Role.query.filter_by(name=role_name).first()
    if not role:
      raise ValueError("Role not found")
    existing = UserRole.query.filter_by(user_id=user_id, role_id=role.id).first()
    if existing:
      raise ValueError("Role already assigned to this user.")
    
    try:
      ur = UserRole(user_id=user_id, role_id=role.id)
      db.session.add(ur)
      db.session.commit()
      return ur   # Not propogated by controller
    except ValueError as error:
      db.session.rollback()
      raise ValueError(str(error)) from error
    except Exception as error:
      db.session.rollback()
      raise ValueError("Invalid data") from error
    
  @staticmethod
  def remove_role(user_id, role_name):
    role = UserRole.query.filter_by(name=role_name).first()
    if not role:
      raise ValueError("Role not found")
    
    instance = UserRole.query.filter_by(user_id=user_id, role_id=role.id).first()
    
    if not instance:
      return "Not Found"
    
    try:
      db.session.delete(instance)
      db.session.commit()
      return "Success"
    except Exception:
      db.session.rollback()
      return "Failed to delete"
    