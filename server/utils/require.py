"""This file exports a decorator function. 
Decorator functions takes in a function as a parameter - Concept is Functional programming
All boillerplate code (wraps).
"""
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from services.user_service import UserService
from utils.errors import AppError, AuthorizationError

def _current_user_id():
  return get_jwt_identity()

def require_admin(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    try:
      roles = UserService.get_roles_for_user(user_id=_current_user_id())
      if "admin" not in roles:
        raise AuthorizationError("Unauthorized: Admin role required")
      return f(*args, **kwargs)
    except AppError as error:
      return {"error": error.message}, error.status_code

  return decorated

def require_admin_or_host(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    try:
      roles = UserService.get_roles_for_user(user_id=_current_user_id())
      if "admin" not in roles and "host" not in roles:
        raise AuthorizationError("Permission denied")
      return f(*args, **kwargs)
    except AppError as error:
      return {"error": error.message}, error.status_code
    
  return decorated 

"""
The way decorators work is that they are chains.
It calls the first decorator, and daisy-chains to the next decorator.
Or you can break the cycle. We want the cycle to keep going and call the next one in the list.
It's like middleware.
"""