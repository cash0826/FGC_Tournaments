from models import Tournament
from .base_service import BaseService
from datetime import datetime
from utils.errors import ValidationError

class TournamentService(BaseService):
  model = Tournament
  
  @classmethod
  def create_tournament(cls, event_id, data):
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")

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
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")

    try:
      if "start" in data and isinstance(data["start"], str):
        data["start"] = datetime.fromisoformat(data["start"])
      if "registration_deadline" in data and isinstance(data["registration_deadline"], str):
        data["registration_deadline"] = datetime.fromisoformat(data["registration_deadline"])
    except ValueError as error:
      raise ValidationError(f"{error}") from error
    
    return super().update(instance_id, data)