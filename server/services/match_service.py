from datetime import datetime

from models import Match, MatchStatuses, TournamentCompetitor
from .base_service import BaseService
from utils.errors import NotFoundError, ValidationError


class MatchService(BaseService):
  model = Match

  @classmethod
  def _get_match(cls, event_id, tournament_id, match_id):
    cls._get_tournament(event_id, tournament_id)
    if not isinstance(match_id, int) or isinstance(match_id, bool) or match_id < 1:
      raise ValidationError("Match id must be a positive integer.")

    match = cls.model.query.filter_by(
      id=match_id, tournament_id=tournament_id
    ).first()
    if not match:
      raise NotFoundError("Match not found for this tournament.")
    return match

  @classmethod
  def _validate_competitors(
    cls, tournament_id, competitor_a_id, competitor_b_id, winner_id
  ):
    competitor_ids = {
      "Competitor A": competitor_a_id,
      "Competitor B": competitor_b_id,
    }
    for label, competitor_id in competitor_ids.items():
      if (not isinstance(competitor_id, int) or isinstance(competitor_id, bool)
          or competitor_id < 1):
        raise ValidationError(f"{label} id must be a positive integer.")

    if winner_id is not None and (
      not isinstance(winner_id, int) or isinstance(winner_id, bool) or winner_id < 1
    ):
      raise ValidationError("Winner id must be a positive integer.")
    if winner_id is not None and winner_id not in competitor_ids.values():
      raise ValidationError("Winner must be one of the match competitors.")

    existing_ids = {
      competitor.id
      for competitor in TournamentCompetitor.query.filter(
        TournamentCompetitor.id.in_(competitor_ids.values()),
        TournamentCompetitor.tournament_id == tournament_id,
      ).all()
    }
    for label, competitor_id in competitor_ids.items():
      if competitor_id not in existing_ids:
        raise ValidationError(
          f"{label} must belong to the match tournament."
        )

  @classmethod
  def _normalize_status(cls, value):
    if isinstance(value, MatchStatuses):
      return value
    if isinstance(value, str):
      normalized = value.strip().casefold()
      for status in MatchStatuses:
        if normalized in (status.value.casefold(), status.name.casefold()):
          return status
    raise ValidationError(
      "Status must be 'Pending', 'In Progress', 'Canceled', or 'Completed'."
    )

  @classmethod
  def _normalize_start_time(cls, value):
    if isinstance(value, str):
      try:
        return datetime.fromisoformat(value)
      except ValueError as error:
        raise ValidationError("Start time must be a valid ISO-8601 datetime.") from error
    return value

  @classmethod
  def get_all(cls, event_id, tournament_id):
    cls._get_tournament(event_id, tournament_id)
    return super().get_all(filters={"tournament_id": tournament_id})

  @classmethod
  def create(cls, event_id, tournament_id, data):
    cls._get_tournament(event_id, tournament_id)
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")

    unsupported_fields = data.keys() - {
      "tournament_id", "round", "start_time", "status",
      "competitor_a_id", "competitor_b_id", "winner_id",
    }
    if unsupported_fields:
      raise ValidationError(
        f"Match fields cannot be set: {', '.join(sorted(unsupported_fields))}."
      )
    if "tournament_id" in data and data["tournament_id"] != tournament_id:
      raise ValidationError("Tournament id must match the request path.")

    match_data = dict(data)
    match_data.pop("tournament_id", None)
    match_data["start_time"] = cls._normalize_start_time(
      match_data.get("start_time")
    )
    match_data["status"] = cls._normalize_status(
      match_data.get("status", MatchStatuses.PENDING)
    )
    cls._validate_competitors(
      tournament_id,
      match_data.get("competitor_a_id"),
      match_data.get("competitor_b_id"),
      match_data.get("winner_id"),
    )
    match_data["tournament_id"] = tournament_id
    return super().create(match_data)

  @classmethod
  def update(cls, event_id, tournament_id, data):
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")
    if "match_id" not in data:
      raise ValidationError("Match id is required.")

    match = cls._get_match(event_id, tournament_id, data["match_id"])
    unsupported_fields = data.keys() - {
      "match_id", "tournament_id", "round", "start_time", "status",
      "competitor_a_id", "competitor_b_id", "winner_id",
    }
    if unsupported_fields:
      raise ValidationError(
        f"Match fields cannot be updated: {', '.join(sorted(unsupported_fields))}."
      )
    if "tournament_id" in data and data["tournament_id"] != tournament_id:
      raise ValidationError("Tournament id must match the request path.")

    match_data = dict(data)
    match_data.pop("match_id")
    match_data.pop("tournament_id", None)
    if "start_time" in match_data:
      match_data["start_time"] = cls._normalize_start_time(match_data["start_time"])
    if "status" in match_data:
      match_data["status"] = cls._normalize_status(match_data["status"])

    cls._validate_competitors(
      tournament_id,
      match_data.get("competitor_a_id", match.competitor_a_id),
      match_data.get("competitor_b_id", match.competitor_b_id),
      match_data.get("winner_id", match.winner_id),
    )
    return super().update(match.id, match_data)

  @classmethod
  def delete(cls, event_id, tournament_id, match_id):
    match = cls._get_match(event_id, tournament_id, match_id)
    return super().delete(match.id)
