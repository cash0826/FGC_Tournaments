from models import LineUpTypes, TournamentCompetitor
from .base_service import BaseService
from utils.errors import NotFoundError, ValidationError

class TournamentCompetitorService(BaseService):
  model = TournamentCompetitor
  
  @classmethod
  def get_tournament_competitor_by_id(cls, event_id, tournament_id, tournament_competitor_id):
    cls._get_tournament(event_id, tournament_id)
    instance = cls.model.query.filter_by(id=tournament_competitor_id)
    if not instance:
      raise NotFoundError("Tournament Competitor not found.")
    return instance
  
  @classmethod
  def add_competitor(cls, event_id, tournament_id, data):
    tournament = cls._get_tournament(event_id, tournament_id)
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
    if tournament.line_up_type == LineUpTypes.SINGLES and user_id is None:
      raise ValidationError("Singles tournaments require a user_id.")
    if tournament.line_up_type == LineUpTypes.TEAM and team_id is None:
      raise ValidationError("Team tournaments require a team_id.")
    if tournament.line_up_type not in (LineUpTypes.SINGLES, LineUpTypes.TEAM):
      raise ValidationError("Tournament lineup type does not support competitors.")

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