from models import Team
from .base_service import BaseService
from utils.errors import NotFoundError, ValidationError

class TeamService(BaseService):
  model = Team
  
  @classmethod
  def get_team_by_name(cls, team_name):   # Searches team using a string instead of an id
    return cls.model.query.filter_by(name=team_name).first()
    
  @classmethod
  def delete(cls, team_name):
    if not isinstance(team_name, str) or not team_name.strip():
      raise ValidationError("Team name is required")
    team_name_normalized = team_name.strip()
    
    instance = TeamService.get_team_by_name(team_name_normalized)
    if not instance:
      raise NotFoundError(f"{team_name} team was not found")
    
    return super().delete(instance.id)