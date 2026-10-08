from models import Standing, TournamentCompetitor
from .base_service import BaseService
from utils.errors import ValidationError
from extensions import db

class StandingService(BaseService):
  model = Standing
  
  # get_standings for competitor
  @classmethod
  def get_standings_for_competitor(cls, competitor_id):
    if not isinstance(competitor_id, int) or isinstance(competitor_id, bool) or competitor_id < 1:
      raise ValidationError("Tournament Competitor id must be a positive integer")

    competitors = (
      db.session.query(TournamentCompetitor.id)
    )
  
  # @classmethod
  # def get_all(cls, event_id, tournament_id):
    pass
    # query tournament
    # event exist in tournament, if not raise NOTFOUND
    # 
    
    # return super().get_all()
  