from extensions import db
from sqlalchemy.orm import validates
from datetime import datetime, timezone

class Team(db.Model):
  __tablename__ = "teams"
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  logo_url = db.Column(db.String, nullable=True)
  created_at = db.Column(db.DateTime, default=db.func.now())
  
  # TODO: Teams are composed of team_members
  
  @validates("name")
  def validates_name(self, key, value):
    if not isinstance(value, str):
      raise ValueError(f"Team name must be a string")
    cleaned = value.strip()
    return cleaned
  
  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "logo_url": self.logo_url,
      "created_at": self.created_at.isoformat()
    }
  
  