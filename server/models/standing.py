from extensions import db
from sqlalchemy.orm import validates

class Standing(db.Model):
  __tablename__ = "standings"
  __table_args__ = (
    db.UniqueConstraint("id", "tournament_competitor_id", name="uq_standings_id_tournament_competitor"),
  )
  
  id = db.Column(db.Integer, primary_key=True)
  tournament_competitor_id = db.Column(db.Integer, db.ForeignKey("tournament_competitors.id"), nullable=False)
  points = db.Column(db.Integer, nullable=True)
  rank = db.Column(db.Integer, nullable=True)
  updated_at = db.Column(db.DateTime, default=db.func.now())
  
  # Relationships
  tournament_competitor = db.relationship("TournamentCompetitor", back_populates="standings_in_tournaments")
  
  @validates("tournament_competitor_id", "points", "rank")
  def validates_ids(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
  def to_dict(self):
    return {
      "tournament_competitor_id": self.tournament_competitor_id,
      "points": self.points,
      "rank": self.rank,
      "updated_at": self.updated_at
    }