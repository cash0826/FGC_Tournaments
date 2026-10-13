from extensions import db
from sqlalchemy.orm import validates
from enum import Enum

class MatchStatuses(Enum):
  PENDING = "Pending"
  IN_PROGRESS = "In Progress"
  CANCELED = "Canceled"
  COMPLETED = "Completed"

class Match(db.Model):
  __tablename__ = "matches"
  __table_args__ = (
    db.ForeignKeyConstraint(
      ["competitor_a_id", "tournament_id"],
      ["tournament_competitors.id", "tournament_competitors.tournament_id"],
      name="fk_matches_competitor_a_tournament",
    ),
    db.ForeignKeyConstraint(
      ["competitor_b_id", "tournament_id"],
      ["tournament_competitors.id", "tournament_competitors.tournament_id"],
      name="fk_matches_competitor_b_tournament",
    ),
    db.CheckConstraint(
      "winner_id IS NULL OR winner_id = competitor_a_id OR winner_id = competitor_b_id",
      name="ck_matches_winner_is_competitor",
    ),
  )
  
  id = db.Column(db.Integer, primary_key=True)
  tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
  round = db.Column(db.String(20), nullable=False)
  start_time = db.Column(db.DateTime)
  status = db.Column(db.Enum(MatchStatuses), default=MatchStatuses.PENDING)
  competitor_a_id = db.Column(db.Integer, db.ForeignKey("tournament_competitors.id"), nullable=False)
  competitor_b_id = db.Column(db.Integer, db.ForeignKey("tournament_competitors.id"), nullable=False)
  winner_id = db.Column(db.Integer, db.ForeignKey("tournament_competitors.id"))
  
  # Belongs to tournament
  tournament = db.relationship("Tournament", back_populates="matches")
  
  # Has one of each: competitor_a, competitor_b, and a winner
  competitor_a = db.relationship(
    "TournamentCompetitor",
    back_populates="matches_as_competitor_a",
    foreign_keys=[competitor_a_id],
  )
  competitor_b = db.relationship(
    "TournamentCompetitor",
    back_populates="matches_as_competitor_b",
    foreign_keys=[competitor_b_id],
  )
  winner = db.relationship(
    "TournamentCompetitor",
    back_populates="matches_won",
    foreign_keys=[winner_id],
  )
  
  @validates("tournament_id", "competitor_a_id", "competitor_b_id", "winner_id")
  def validates_ids(self, key, value):
    if value is None and key == "winner_id":
      return value
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
  def to_dict(self):
    return {
      "tournament_id": self.tournament_id,
      "round": self.round,
      "start_time": self.start_time,
      "status": self.status,
      "competitor_a_id": self.competitor_a_id,
      "competitor_b_id": self.competitor_b_id,
      "winner_id": self.winner_id
    }