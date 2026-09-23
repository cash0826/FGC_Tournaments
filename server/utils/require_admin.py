"""Exports a decorator function. 
Takes a function as a parameter.
All boillerplate code.
"""
from functools import wraps

def require_admin(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    pass
  