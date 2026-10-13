from models import Bracket
from .base_service import BaseService
from utils.errors import NotFoundError, ValidationError

class BracketService(BaseService):
  model = Bracket

  @classmethod
  def get_bracket(cls, event_id, tournament_id):
    cls._get_tournament(event_id, tournament_id)
    instance = cls.model.query.filter_by(tournament_id=tournament_id).first()
    if not instance:
      raise NotFoundError("Bracket not found.")
    return instance

  @classmethod
  def get_bracket_by_id(cls, event_id, tournament_id, bracket_id):
    cls._get_tournament(event_id, tournament_id)
    if not isinstance(bracket_id, int) or isinstance(bracket_id, bool) or bracket_id < 1:
      raise ValidationError("Bracket id must be a positive integer.")

    instance = cls.model.query.filter_by(
      id=bracket_id, tournament_id=tournament_id
    ).first()
    if not instance:
      raise NotFoundError("Bracket not found for this tournament.")
    return instance

  @classmethod
  def create_bracket(cls, event_id, tournament_id, data):
    cls._get_tournament(event_id, tournament_id)
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")

    unsupported_fields = data.keys() - {"url", "tournament_id"}
    if unsupported_fields:
      raise ValidationError(
        f"Bracket fields cannot be set: {', '.join(sorted(unsupported_fields))}."
      )
    if ("tournament_id" in data
        and data["tournament_id"] != tournament_id):
      raise ValidationError("Tournament id must match the request path.")

    bracket_data = {"tournament_id": tournament_id}
    if "url" in data:
      bracket_data["url"] = data["url"]
    return super().create(bracket_data)

  @classmethod
  def update_bracket(cls, event_id, tournament_id, bracket_id, data):
    bracket = cls.get_bracket_by_id(event_id, tournament_id, bracket_id)
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")

    unsupported_fields = data.keys() - {"url"}
    if unsupported_fields:
      raise ValidationError(
        f"Bracket fields cannot be updated: {', '.join(sorted(unsupported_fields))}."
      )
    return super().update(bracket.id, data)

  @classmethod
  def delete_bracket(cls, event_id, tournament_id, bracket_id):
    bracket = cls.get_bracket_by_id(event_id, tournament_id, bracket_id)
    return super().delete(bracket.id)