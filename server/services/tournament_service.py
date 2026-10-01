from models import Tournament, GamingPlatform, LineUpTypes
from .base_service import BaseService
from datetime import datetime

class TournamentService(BaseService):
  model = Tournament
  
  @classmethod
  def create_tournament(cls, event_id, data):
    try:
      if "start" in data and isinstance(data["start"], str):
        data["start"] = datetime.fromisoformat(data["start"])
      if "registration_deadline" in data and isinstance(data["registration_deadline"], str):
        data["registration_deadline"] = datetime.fromisoformat(data["registration_deadline"])
    except ValueError as error:
      raise ValidationError(f"{error}") from error
    
    data["event_id"] = event_id
    return super().create(data)

  @classmethod
  def update_tournament(cls, instance_id, data):
    try:
      if "start" in data and isinstance(data["start", str]):
        data["start"] = datetime.fromisoformat(data["start"])
      if "registration_deadline" in data and isinstance(data["registration_deadline"], str):
        data["registration_deadline"] = datetime.fromisoformat(data["registration_deadline"])
    except ValueError as error:
      raise ValidationError(f"{error}") from error
    
    return super().update(instance_id, data)