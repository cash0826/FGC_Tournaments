from models import LineUpTypes, Standing, Team, TournamentCompetitor, User
from .base_service import BaseService
from utils.errors import ValidationError
from extensions import db

class StandingService(BaseService):
  model = Standing
  
  @classmethod
  def _get_standing(cls, event_id, tournament_id, competitor_id):
    cls._get_tournament(event_id, tournament_id)
    if not isinstance(competitor_id, int) or competitor_id < 1:
      raise ValidationError("Competitor id must be a positive integer")
    
    standing = cls.model.query.filter_by(
      id=competitor_id, tournament_id=tournament_id
    ).first()
    
    if not standing:
      raise NotFoundError("Standing not found for this competitor")
    return standing

  @classmethod
  def add_for_competitor(cls, competitor):
    if not isinstance(competitor, TournamentCompetitor):
      raise ValidationError("A tournament competitor is required to create a standing.")

    standing = Standing(tournament_competitor=competitor)
    db.session.add(standing)
    return standing
  
  @classmethod
  def _serialize_competitors(cls, rows, name_field):
    return [
      {
        **competitor.to_dict(),
        "id": competitor.id,
        name_field: name,
        "standing": standing.to_dict() if standing else None,
      }
      for competitor, name, standing in rows
    ]

  @classmethod
  def get_standings_for_all_teams(cls, tournament_id):
    rows = (
      db.session.query(TournamentCompetitor, Team.name, Standing)
      .outerjoin(Team, TournamentCompetitor.team_id == Team.id)
      .outerjoin(Standing, Standing.tournament_competitor_id == TournamentCompetitor.id)
      .filter(TournamentCompetitor.tournament_id == tournament_id)
      .order_by(TournamentCompetitor.id)
      .all()
    )
    return cls._serialize_competitors(rows, "team_name")

  @classmethod
  def get_standings_for_all_users(cls, tournament_id):
    rows = (
      db.session.query(TournamentCompetitor, User.gamer_name, Standing)
      .outerjoin(User, TournamentCompetitor.user_id == User.id)
      .outerjoin(Standing, Standing.tournament_competitor_id == TournamentCompetitor.id)
      .filter(TournamentCompetitor.tournament_id == tournament_id)
      .order_by(TournamentCompetitor.id)
      .all()
    )
    return cls._serialize_competitors(rows, "gamer_name")
  
  @classmethod
  def get_all(cls, event_id, tournament_id):
    tournament = cls._get_tournament(event_id, tournament_id)
    
    if tournament.line_up_type == LineUpTypes.TEAM:
      return cls.get_standings_for_all_teams(tournament.id)
    if tournament.line_up_type == LineUpTypes.SINGLES:
      return cls.get_standings_for_all_users(tournament.id)
    raise ValidationError("Tournament lineup type does not support competitors.")
  
  @classmethod
  def update(cls, event_id, tournament_id, competitor_id, data):
    standing = cls._get_standing(event_id, tournament_id, competitor_id)
    
    unsupported_fields = data.keys() - {
      "tournament_competitor_id", "points", "rank"
    }
    if unsupported_fields:
      raise ValidationError(
        f"Match fields cannot be updated: {', '.join(sorted(unsupported_fields))}."
      )
    if "tournament_competitor_id" in data and data["tournament_competitor_id"] != competitor_id:
      raise ValidationError("Competitor id must match the request path")
      
    return super().update(standing.id, data)
    