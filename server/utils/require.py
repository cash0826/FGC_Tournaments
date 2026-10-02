from functools import wraps
from flask_jwt_extended import get_jwt_identity
from services import UserService, EventService
from utils.errors import AppError, AuthorizationError

""" Helper functions """

def _current_user_id():
  return get_jwt_identity()

def _roles_for_user():
  return UserService.get_roles_for_user(user_id=int(_current_user_id()))

def require_event_ownership_or_admin(event_id):
  event = EventService.get_by_id(event_id)
  if event.host_id != int(_current_user_id()) and "admin" not in _roles_for_user():
    raise AuthorizationError("Permission denied: Requires event ownership or higher authorization")

""" Decorator functions 
Decorator functions takes in a function as a parameter - Concept is Functional programming
All boillerplate code (wraps).
"""

def require_admin(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    try:
      roles = _roles_for_user()
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
      roles = _roles_for_user()
      if "admin" not in roles and "host" not in roles:
        raise AuthorizationError("Permission denied: Requires authorized account")
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