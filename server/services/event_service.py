from extensions import db
from models import Event, Sponsor, EventSponsor
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
  
  @classmethod
  def get_event_sponsors(cls, event_id):
    cls._get_event(event_id)
    
    sponsors = (
      db.session.query(Sponsor.name)
      .join(EventSponsor, EventSponsor.sponsor_id == Sponsor.id)
      .filter(EventSponsor.event_id == event_id)
      .all()
    )
    return [sponsor[0] for sponsor in sponsors]