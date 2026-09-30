from datetime import datetime

from extensions import db
from sqlalchemy.orm import validates

class Event(db.Model):
  __tablename__ = "events"
  
  id = db.Column(db.Integer, primary_key=True)
  host_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  name = db.Column(db.String(50), nullable=False)
  start = db.Column(db.DateTime, nullable=False)
  end = db.Column(db.DateTime)
  in_person = db.Column(db.Boolean, default=False)
  location = db.Column(db.String)
  description = db.Column(db.Text)
  rules = db.Column(db.Text)
  
  # --------------
  # Relationships
  # --------------
  
  # event belongs to a single user (host)
  host = db.relationship(
    "User", back_populates="hosted_events", foreign_keys=[host_id]
  )
  
  # TODO: event contains tournaments
  
  # --------------
  # Validations
  # --------------
  
  @validates("name", "location", "description", "rules")
  def validate_text(self, key, value):
    if not isinstance(value, str):
      raise ValueError(f"{key} must be a string")
    return value.lower().strip()
  
  @validates("host_id")
  def validates_id(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value

  @validates("in_person")
  def validates_in_person(self, key, value):
    if not isinstance(value, bool):
      raise ValueError(f"in_person must be an boolean")
    return value
  
  @validates("start", "end")
  def validates_datetimes(self, key, value):
    if value is None and key == "end":
      return value
    if not isinstance(value, datetime):
      raise ValueError(f"{key} must be a datetime")

    current_time = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()
    if value < current_time:
      raise ValueError(f"{key} cannot be in the past")
    return value
  
  def to_dict(self):
    return {
      "id": self.id,
      "host_id": self.host_id,
      "name": self.name,
      "start": self.start.isoformat(),
      "end": self.end.isoformat(),
      "in_person": self.in_person,
      "location": self.location,
      "description": self.description,
      "rules": self.rules
    }