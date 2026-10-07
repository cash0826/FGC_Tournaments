from models import Tournament, TournamentCompetitor
from .base_service import BaseService
from utils.errors import NotFoundError, ValidationError

class TournamentCompetitorService(BaseService):
  model = TournamentCompetitor
  
  @classmethod
  def _get_tournament(cls, event_id, tournament_id):
    if not isinstance(event_id, int) or isinstance(event_id, bool) or event_id < 1:
      raise ValidationError("Event id must be a positive integer.")
    if (not isinstance(tournament_id, int) or isinstance(tournament_id, bool)
        or tournament_id < 1):
      raise ValidationError("Tournament id must be a positive integer.")

    tournament = Tournament.query.filter_by(
      id=tournament_id, event_id=event_id
    ).first()
    if not tournament:
      raise NotFoundError("Tournament not found for this event.")
    return tournament
  
  @classmethod
  def get_tournament_competitor_by_id(cls, event_id, tournament_id, tournament_competitor_id):
    cls._get_tournament(event_id, tournament_id)
    instance = cls.model.query.filter_by(id=tournament_competitor_id)
    if not instance:
      raise NotFoundError("Tournament Competitor not found.")
    return instance
  
  @classmethod
  def add_competitor(cls, event_id, tournament_id, data):
    cls._get_tournament(event_id, tournament_id)
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")
    unsupported_fields = data.keys() - {"team_id", "user_id", "seed", "tournament_id"}
    if unsupported_fields:
      raise ValidationError(
        f"Tournament competitor fields cannot be set: "
        f"{', '.join(sorted(unsupported_fields))}."
      )
    if "tournament_id" in data and data["tournament_id"] != tournament_id:
      raise ValidationError("Tournament id must match the request path.")

    team_id = data.get("team_id")
    user_id = data.get("user_id")
    if (team_id is None) == (user_id is None):
      raise ValidationError(
        "Exactly one of team_id or user_id must be provided."
      )
    entry_id = team_id if team_id is not None else user_id
    if not isinstance(entry_id, int) or isinstance(entry_id, bool) or entry_id < 1:
      entry_type = "Team" if team_id is not None else "User"
      raise ValidationError(f"{entry_type} id must be a positive integer.")

    competitor_data = {
      "tournament_id": tournament_id,
      "team_id": team_id,
      "user_id": user_id,
    }
    if "seed" in data:
      competitor_data["seed"] = data["seed"]
    return super().create(competitor_data)
  
  @classmethod
  def remove_competitor(cls, event_id, tournament_id, data):
    tournament_competitor_id = data.get("tournament_competitor_id")
    competitor = cls.get_tournament_competitor_by_id(event_id, tournament_id, tournament_competitor_id)
    return super().delete(competitor.id)