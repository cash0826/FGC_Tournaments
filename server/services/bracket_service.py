from models import Bracket
from .base_service import BaseService
from utils.errors import NotFoundError

class BracketService(BaseService):
  model = Bracket
  
  @classmethod
  def get_bracket(cls, event_id, tournament_id):
    instance = cls.model.query.filter_by(tournament_id=tournament_id).first()
    if not instance:
      raise NotFoundError(f"Bracket not found.")
    return instance