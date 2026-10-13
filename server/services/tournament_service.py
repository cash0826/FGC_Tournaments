from models import Tournament
from .base_service import BaseService
from datetime import datetime
from utils.errors import ValidationError

class TournamentService(BaseService):
  model = Tournament
  
  @classmethod
  def get_all(cls, event_id):
    cls._get_event(event_id)
    return super().get_all(filters={"event_id": event_id})
    
  @classmethod
  def create_tournament(cls, event_id, data):
    cls._get_event(event_id)
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")
    
    unsupported_fields = data.keys() - {
      "game_id", "name", "start", "registration_deadline",
      "gaming_platform", "line_up_type"
    }
    if unsupported_fields:
      raise ValidationError(
        f"Event fields cannot be set: {', '.join(sorted(unsupported_fields))}."
      )
      
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
  def update_tournament(cls, event_id, tournament_id, data):
    tournament = cls._get_tournament(event_id, tournament_id)
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")
    
    unsupported_fields = data.keys() - {
      "name", "start", "registration_deadline",
      "gaming_platform"
    }
    if unsupported_fields:
      raise ValidationError(
        f"Event fields cannot be set: {', '.join(sorted(unsupported_fields))}."
      )
      
    try:
      if "start" in data and isinstance(data["start"], str):
        data["start"] = datetime.fromisoformat(data["start"])
      if "registration_deadline" in data and isinstance(data["registration_deadline"], str):
        data["registration_deadline"] = datetime.fromisoformat(data["registration_deadline"])
    except ValueError as error:
      raise ValidationError(f"{error}") from error
    
    return super().update(tournament.id, data)
  
  @classmethod
  def delete(cls, event_id, tournament_id):
    tournament = cls._get_tournament(event_id, tournament_id)
    return super().delete(tournament.id)