from extensions import db
from sqlalchemy.orm import validates

# __table_args__: Exactly one of team_id or user_id is needed. Rejects if both are provided

class TournamentCompetitor(db.Model):
  __tablename__ = "tournament_competitors"
  __table_args__ = (
    db.CheckConstraint(
      "(team_id IS NOT NULL AND user_id IS NULL) OR "
      "(team_id IS NULL AND user_id IS NOT NULL)",
      name="ck_tournament_competitors_exactly_one_entry",
    ),
    db.UniqueConstraint("id", "tournament_id", name="uq_tournament_competitors_id_tournament"),
  )
  
  id = db.Column(db.Integer, primary_key=True)
  tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
  team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
  seed = db.Column(db.Integer, nullable=True)
  
  # competitors are registered to a single tournament / belongs to tournament
  tournament = db.relationship(
    "Tournament", back_populates="competitors", foreign_keys=[tournament_id]
  )
  
  # tournament_competitor is assigned to a team (or user)
  team = db.relationship(
    "Team", back_populates="team_tournaments", foreign_keys=[team_id]
  )
  
  # tournament_competitor is assigned to a user (or team)
  user = db.relationship(
    "User", back_populates="solo_tournaments", foreign_keys=[user_id]
  )

  # Matches where this competitor appears or wins
  matches_as_competitor_a = db.relationship(
    "Match", back_populates="competitor_a", foreign_keys="Match.competitor_a_id"
  )
  matches_as_competitor_b = db.relationship(
    "Match", back_populates="competitor_b", foreign_keys="Match.competitor_b_id"
  )
  matches_won = db.relationship(
    "Match", back_populates="winner", foreign_keys="Match.winner_id"
  )
  
  @validates("tournament_id", "team_id", "user_id")
  def validates_ids(self, key, value):
    if value is None and key in ("team_id", "user_id"):
      return value
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    if key == "team_id" and self.user_id is not None:
      raise ValueError("Exactly one of team_id or user_id must be set")
    if key == "user_id" and self.team_id is not None:
      raise ValueError("Exactly one of team_id or user_id must be set")
    return value
  
  def to_dict(self):
    return {
      "tournament_id": self.tournament_id,
      "team_id": self.team_id,
      "user_id": self.user_id,
      "seed": self.seed
    }