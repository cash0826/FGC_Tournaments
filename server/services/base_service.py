from extensions import db
from sqlalchemy.exc import IntegrityError
from utils.errors import AppError, ConflictError, NotFoundError, ValidationError

"""Assist with CRUD boilerplate code
Allows overrides
Controllers call: [].create, [].get_by_id(), [].get_all(), [].update(), and [].delete()"""

class BaseService:
  model = None    # Subclasses must set this
  
  @classmethod
  def get_by_id(cls, instance_id):
    instance = cls.model.query.filter_by(id=instance_id).first()
    if not instance:
      raise NotFoundError(f"{cls.model.__name__} not found.")
    return instance
  
  @classmethod
  def get_all(cls, filters=None):
    q = cls.model.query
    if filters:
      q = q.filter_by(**filters)
    return q
  
  @classmethod
  def create(cls, data):
    try:
      new = cls.model(**data)
      db.session.add(new)
      db.session.commit()
    except IntegrityError as error:
      db.session.rollback()
      raise ConflictError(f"{error}") from error
    except ValueError as error:
      db.session.rollback()
      raise ValidationError(str(error)) from error
    except Exception as error:
      db.session.rollback()
      raise AppError(f"{error}", 500) from error
    
    return new
  
  @classmethod
  def update(cls, instance_id, data):
    instance = cls.get_by_id(instance_id)
    
    if not instance:
      raise NotFoundError(f"{instance_id} not found")
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")
    
    try:
      for key, value in data.items():
        setattr(instance, key, value)
      db.session.commit()
    except IntegrityError as error:
      db.session.rollback()
      raise ConflictError(f"{error}") from error
    except ValueError as error:
      db.session.rollback()
      raise ValidationError(str(error)) from error
    except Exception as error:
      db.session.rollback()
      raise AppError(f"{error}", 500) from error
      
    return instance
  
  @classmethod
  def delete(cls, instance_id):
    instance = cls.get_by_id(instance_id)
    
    if not instance:
      raise NotFoundError(f"{instance_id} not found")
    
    try:
      db.session.delete(instance)
      db.session.commit()
    except Exception as error:
      db.session.rollback()
      raise AppError(f"{error}", 500) from error
