from extensions import db
from models import Event
from .base_service import BaseService
from utils.errors import NotFoundError, ValidationError
from datetime import datetime

class EventService(BaseService):
  model = Event
  
  @classmethod
  def create_event(cls, user_id, data):
    try:
      if 'start' in data and isinstance(data['start'], str):
        data['start'] = datetime.fromisoformat(data['start'])
      if 'end' in data and isinstance(data['end'], str):
        data['end'] = datetime.fromisoformat(data['end'])
    except ValueError as error:
      raise ValidationError(f"{error}") from error
    
    data["host_id"] = user_id
    return super().create(data)
  
  @classmethod
  def update_event(cls, instance_id, data):
    try:
      if 'start' in data and isinstance(data['start'], str):
        data['start'] = datetime.fromisoformat(data['start'])
      if 'end' in data and isinstance(data['end'], str):
        data['end'] = datetime.fromisoformat(data['end'])
    except ValueError as error:
      raise ValidationError(f"{error}") from error
    
    return super().update(instance_id, data)