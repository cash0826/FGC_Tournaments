from extensions import db
from sqlalchemy.orm import validates

# One to One (only 1 bracket x tournament)

class Bracket(db.Model):
  __tablename__ = "bracket"
  
  id = db.Column(db.Integer, primary_key=True)
  tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
  url = db.Column(db.Text)
  
  # bracket is scheduled by (belongs to) tournament
  tournament = db.relationship(
    "Tournament", back_populates="bracket", foreign_keys=[tournament_id]
  )
  
  # Validation
  @validates("tournament_id")
  def validate_tournament_id(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"Tournament id must be an integer")
    return value
  
  def to_dict(self):
    return {
      "id": self.id,
      "tournament_id": self.tournament_id,
      "url": self.url
    }