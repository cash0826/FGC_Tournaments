from models import Team
from .base_service import BaseService
from utils.errors import NotFoundError, ValidationError

class TeamService(BaseService):
  model = Team
  
  # @classmethod
  # def get_team_by_name(cls, team_name):   # Searches team using a string instead of an id
  #   return cls.model.query.filter_by(name=team_name).first()
  
  @classmethod
  def create(cls, data):
    unsupported_fields = data.keys() - {"name", "logo_url", "team"}
    if unsupported_fields:
      raise ValidationError(
        f"Team fields cannot be set: "
        f"{', '.join(sorted(unsupported_fields))}."
      )
    
    return super().create(data)
  
  @classmethod
  def update(cls, team_id, data):
    unsupported_fields = data.keys() - {"name", "logo_url", "team"}
    if unsupported_fields:
      raise ValidationError(
        f"Team fields cannot be set: "
        f"{', '.join(sorted(unsupported_fields))}."
      )
    team_data = dict(data)
    team_data.pop("team")
    return super().update(team_id, team_data)